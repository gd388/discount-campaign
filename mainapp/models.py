# models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()



class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('cart', 'Cart'),
        ('delivery', 'Delivery-specific'),
    )

    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    used_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_usage_per_customer_per_day = models.IntegerField(default=1)
    eligible_customers = models.ManyToManyField(User, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.used_budget < self.budget

    def __str__(self):
        return self.name

class DiscountUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    date = models.DateField()
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'discount', 'date')