GET /discounts/
    - List all discount campaigns

GET /discounts/available/
    - List discounts available to the current user (based on date, budget, eligibility)

POST /discounts/
    - Create a discount campaign
    - Fields: name, discount_type, budget, start_date, end_date, max_usage_per_customer_per_day

PATCH /discounts/{id}/
    - Update discount

DELETE /discounts/{id}/
    - Delete discount
"""