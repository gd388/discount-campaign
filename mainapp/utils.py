from datetime import date
from django.utils import timezone 
from .models import DiscountUsage

def can_use_discount(user, discount):
    now = timezone.now()
    if not (discount.start_date <= now <= discount.end_date):
        return False, "Discount is not active"

    if discount.used_budget >= discount.budget:
        return False, "Discount budget exhausted."

    if discount.eligible_customers.exists() and user not in discount.eligible_customers.all():
        return False, "User is not eligible for this discount"

    

    return True, "Discount is valid"
