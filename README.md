# Minimalistic Backend Web App for Online Shop

This project is a Python-based backend API for a minimalistic online shop, built using Flask and SQLAlchemy with SQLite for data persistence. It provides CRUD (Create, Read, Update, Delete) operations for Customers, Shop Item Categories, Shop Items, and Orders.

## Project Structure

```
.
├── app/                        # Main application package
│   ├── __init__.py             # Application factory (create_app)
│   ├── models/                 # SQLAlchemy data models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routes/                 # API Blueprints for each entity
│   │   ├── __init__.py
│   │   ├── category_routes.py
│   │   ├── customer_routes.py
│   │   ├── item_routes.py
│   │   └── order_routes.py
│   └── utils/                  # Utility functions (e.g., database initialization)
│       ├── __init__.py
│       └── db_utils.py
├── instance/                   # Instance folder (SQLite DB will be created here)
│   └── shop.sqlite             # (auto-generated on run)
├── tests/                      # Pytest tests
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and test app setup
│   ├── test_category_api.py
│   ├── test_customer_api.py
│   ├── test_item_api.py
│   └── test_order_api.py
├── requirements.txt            # Python package dependencies
├── run.py                      # Script to run the Flask application
└── README.md                   # This file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**
    Make sure your virtual environment is activated, then run:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the setup is complete, you can run the Flask application using the `run.py` script:

```bash
python run.py
```

The application will start, and by default, it will be accessible at `http://127.0.0.1:5000/`.

When the application starts for the first time:
*   The SQLite database file (`instance/shop.sqlite`) will be created.
*   Database tables will be created based on the defined models.
*   Initial test data will be populated into the database. (This includes sample customers, categories, items, and orders).

## Running Tests

This project uses Pytest for running automated tests. To run the tests:

1.  Ensure your virtual environment is activated and all dependencies (including `pytest`) are installed.
2.  Navigate to the root directory of the project.
3.  Run the following command:

    ```bash
    pytest
    ```
    Or, for more verbose output:
    ```bash
    pytest -v
    ```

Tests are located in the `tests/` directory and cover all API endpoints. They run against an in-memory SQLite database, ensuring that the main development database is not affected.

## API Endpoints

The API provides CRUD operations for the following entities. Base URLs are:
*   Customers: `/customers`
*   Shop Item Categories: `/categories`
*   Shop Items: `/items`
*   Orders: `/orders`

Refer to the route files in `app/routes/` for details on specific endpoints (e.g., `GET /customers/<id>`, `POST /items`, etc.) and expected request/response formats (JSON).

### Data Entities

*   **Customer**: `id`, `name`, `surname`, `email`
*   **ShopItemCategory**: `id`, `title`, `description`
*   **ShopItem**: `id`, `title`, `description`, `price`, `categories` (list of ShopItemCategory)
*   **OrderItem**: `id`, `shop_item` (ShopItem), `quantity`
*   **Order**: `id`, `customer` (Customer), `items` (list of OrderItem)

All primary keys (`id`) are integers. Relationships are handled as described (e.g., an Order contains a Customer object and a list of OrderItem objects in its JSON representation).
When creating or updating entities that reference other entities (e.g., creating an Order requires a `customer_id`; creating a ShopItem can take `category_ids`), provide the IDs of the related entities.
```
