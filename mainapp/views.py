# views.py

from django.utils import timezone
from .models import Discount, DiscountUsage
from .serializers import DiscountSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated,]

    def validate_discount(self, validated_data):
        if validated_data['end_date'] < timezone.now():
            raise serializers.ValidationError("End date must be in the future.")
        if validated_data['budget'] <= 0:
            raise serializers.ValidationError("Budget must be greater than zero.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_discount(serializer.validated_data)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.validate_discount(serializer.validated_data)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='available')
    def available_discounts(self, request):
        user = request.user
        now = timezone.now()
        discounts = Discount.objects.filter(
            start_date__lte=now,
            end_date__gte=now,
            used_budget__lt=Discount.F('budget'),
        )

        if user.is_authenticated:
            discounts = discounts.filter(
                Discount.Q(eligible_customers__isnull=True) |
                Discount.Q(eligible_customers=user)
            ).distinct()

        serializer = self.get_serializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='apply')



    def apply_discount(self, request, pk=None):
        discount = self.get_object()
        user = request.user

        cart_total = Decimal(request.data.get("cart_total", "0"))
        delivery_charge = Decimal(request.data.get("delivery_charge", "0"))

        # Check discount eligibility and daily usage
        from .utils import can_use_discount
        can_use, message = can_use_discount(user, discount)
        if not can_use:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()
        usage, _ = DiscountUsage.objects.get_or_create(
            user=user,
            discount=discount,
            date=today
        )
        
        if usage.usage_count >= discount.max_usage_per_customer_per_day:
            return Response({"error": "You have exceeded the maximum number of uses for today."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if remaining budget is sufficient
        remaining_budget = discount.budget - discount.used_budget
        if remaining_budget <= 0:
            return Response({"error": "Discount budget exhausted."}, status=status.HTTP_400_BAD_REQUEST)

        # Apply discount
        discount_amount = Decimal('0.0')
        if discount.discount_type == "cart":
            discount_value = cart_total * Decimal('0.1')
            discount_amount = min(remaining_budget, discount_value)
            cart_total -= discount_amount

        elif discount.discount_type == "delivery":
            discount_value = delivery_charge * Decimal('0.2')
            discount_amount = min(remaining_budget, discount_value)
            delivery_charge -= discount_amount

        # Update usage and budget
        usage.usage_count += 1
        usage.save()

        discount.used_budget += discount_amount
        discount.save()

        return Response({
            "cart_total": round(cart_total, 2),
            "delivery_charge": round(delivery_charge, 2),
            "discount_applied": round(discount_amount, 2),
            "discount_type": discount.discount_type,
            "remaining_usage_today": discount.max_usage_per_customer_per_day - usage.usage_count,
            
        })
