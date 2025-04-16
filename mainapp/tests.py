from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Discount, DiscountUsage
from decimal import Decimal
from datetime import timedelta

User = get_user_model()

class DiscountApplyTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.discount = Discount.objects.create(
            name="Test Cart Discount",
            discount_type="cart",
            budget=Decimal("100.00"),
            used_budget=Decimal("0.00"),
            max_usage_per_customer_per_day=2,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )
        self.discount.eligible_customers.add(self.user)

    def test_apply_discount_success(self):
        response = self.client.post(f'/discounts/{self.discount.id}/apply/', {
            "cart_total": "50.00",
            "delivery_charge": "10.00"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("discount_applied", response.data)
        self.assertEqual(DiscountUsage.objects.filter(user=self.user, discount=self.discount).count(), 1)
        self.assertEqual(DiscountUsage.objects.get(user=self.user, discount=self.discount).usage_count, 1)

    def test_apply_discount_exceeds_usage_limit(self):
        # Simulate reaching the usage limit
        DiscountUsage.objects.create(user=self.user, discount=self.discount, usage_count=2, date=timezone.now().date())

        response = self.client.post(f'/discounts/{self.discount.id}/apply/', {
            "cart_total": "50.00",
            "delivery_charge": "10.00"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "You have exceeded the maximum number of uses for today.")

    def test_apply_discount_budget_exhausted(self):
        self.discount.used_budget = Decimal("100.00")
        self.discount.save()

        response = self.client.post(f'/discounts/{self.discount.id}/apply/', {
            "cart_total": "50.00",
            "delivery_charge": "10.00"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Discount budget exhausted.")
