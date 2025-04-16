# discount/admin.py
from django.contrib import admin
from .models import Discount,DiscountUsage

class DiscountAdmin(admin.ModelAdmin):
    # Add a search bar for name and discount type
    search_fields = ['name', 'discount_type']
    
    # Display fields in the list view
    list_display = ('id','name', 'discount_type', 'budget', 'used_budget', 'start_date', 'end_date',)
    
# Register the custom admin
admin.site.register(Discount, DiscountAdmin)

class DiscountUsageAdmin(admin.ModelAdmin):
    # Search by username or email (adjust if needed)
    search_fields = ['user__username', 'user__email']

    # Display related user and discount info
    list_display = ('get_username', 'discount', 'date', 'usage_count')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'User'

# Register the admin
admin.site.register(DiscountUsage, DiscountUsageAdmin)