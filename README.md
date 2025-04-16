# Discount Campaign Management

Discount Campaign Management is a Django-based web application for managing and applying discount campaigns. It supports both cart-wide and delivery-specific discounts, with usage limits, budget management, and customer eligibility filters.

## About

Discount Campaign Management enables businesses to create and manage discount campaigns. It offers flexibility to apply discounts in various ways, monitor usage, and enforce budget and usage limits.

### Key Features:
- **Discount Creation**: Allows users to create discount campaigns with configurable start and end dates, budget limits, and customer eligibility.
- **Discount Application**: Apply discounts to a cart's total or delivery charge, ensuring eligibility and budget constraints.
- **Usage Control**: Track and manage the number of times a discount has been used by each customer on a daily basis.
- **Budget Management**: Ensure discounts do not exceed the defined budget, with real-time updates.

## Features

- **Create and Manage Discount Campaigns((CRUD))**: Set up discount campaigns with different types (cart-wide, delivery-specific) and budget constraints.
- **Customer Eligibility**: Target specific customers or allow any customer to access the discount.
- **Daily Usage Limit**: Set a maximum number of uses per customer per day.
- **Budget Management**: Track the used and remaining budget for each discount campaign.
- **Discount Application**: Apply the discount to the cart total or delivery charge based on campaign rules.
  
## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/discount-campaign.git
    cd discount-campaign
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

## Usage

After setting up the project, you can use it by interacting with the Django API or using the admin interface.

### Access the Admin Panel

- Navigate to: `http://127.0.0.1:8000/admin/`
- Login with the superuser credentials.



### Discount Creation via API

- **URL**: `/discounts/`
- **Method**: `POST`
- **Body**:
    ```json
    {
      "name": "Summer Sale",
      "discount_type": "cart",
      "budget": 1000.0,
      "start_date": "2025-05-01T00:00:00Z",
      "end_date": "2025-08-01T00:00:00Z",
      "max_usage_per_customer_per_day": 5,
      "eligible_customers": [1, 2]
    }
    ```
- **Response**:
    ```json
    {
      "id": 1,
      "name": "Summer Sale",
      "discount_type": "cart",
      "budget": 1000.0,
      "used_budget": 0.0,
      "max_usage_per_customer_per_day": 5,
      "start_date": "2025-05-01T00:00:00Z",
      "end_date": "2025-08-01T00:00:00Z",
      "eligible_customers": [1, 2]
    }
    ```

## API Endpoints

### `GET /discounts/`
- **Description**: List all available discount campaigns.
- **cURL Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/discounts/ -H "Authorization: Bearer <JWT_TOKEN>"
    ```

- **Response**:
    ```json
    [
      {
        "id": 1,
        "name": "Summer Sale",
        "discount_type": "cart",
        "budget": 1000.0,
        "used_budget": 200.0,
        "max_usage_per_customer_per_day": 5,
        "start_date": "2025-05-01T00:00:00Z",
        "end_date": "2025-08-01T00:00:00Z",
        "eligible_customers": [1, 2]
      }
    ]
    ```

### `GET /discounts/available/`

- **Description**: List all currently available discount campaigns for the authenticated user (if logged in) or all generally available campaigns.

- **cURL Example**:
  ```bash
  curl -X GET [http://127.0.0.1:8000/discounts/available/](http://127.0.0.1:8000/discounts/available/) -H "Authorization: Bearer <JWT_TOKEN>"
- **Response**:
    ```json
  [
  {
    "id": 2,
    "name": "New Year Blast",
    "discount_type": "cart",
    "budget": 1500.0,
    "used_budget": 300.0,
    "max_usage_per_customer_per_day": 3,
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-01-31T23:59:59Z",
    "eligible_customers": [4, 6]
  },
  {
    "id": 3,
    "name": "Free Delivery April",
    "discount_type": "delivery",
    "budget": 800.0,
    "used_budget": 100.0,
    "max_usage_per_customer_per_day": 2,
    "start_date": "2025-04-01T00:00:00Z",
    "end_date": "2025-04-15T23:59:59Z",
    "eligible_customers": []
  }
]


### `POST /discounts/{id}/apply/`
- **Description**: Apply a discount to a user's cart or delivery charge.
- **cURL Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/discounts/1/apply/ -H "Authorization: Bearer <JWT_TOKEN>" -H "Content-Type: application/json" -d '{
        "cart_total": 100.0,
        "delivery_charge": 10.0
    }'
    ```

- **Response**:
    ```json
    {
      "cart_total": 90.0,
      "delivery_charge": 8.0,
      "discount_applied": 10.0,
      "discount_type": "cart",
      "remaining_usage_today": 4
    }
    ```

## Security

All API endpoints are secured using **JWT** (JSON Web Token) authentication. You need to pass the token in the `Authorization` header of each request.

- Example:
    ```bash
    curl -X GET http://127.0.0.1:8000/discounts/ -H "Authorization: Bearer <JWT_TOKEN>"
    ```

