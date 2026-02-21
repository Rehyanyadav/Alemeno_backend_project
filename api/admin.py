from django.contrib import admin
from .models import Customer, Loan

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'monthly_income', 'approved_limit')
    search_fields = ('first_name', 'last_name', 'phone_number')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'interest_rate', 'tenure', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'loan_id')
