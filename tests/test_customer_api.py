import json
import pytest

# Initial data will create 2 customers. IDs usually start from 1.
# Cust1: John Doe (ID 1), Cust2: Jane Smith (ID 2)

def test_create_customer(client, init_database):
    """Test creating a new customer."""
    response = client.post('/customers', json={
        'name': 'Alice',
        'surname': 'Wonderland',
        'email': 'alice.wonder@example.com'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Alice'
    assert data['email'] == 'alice.wonder@example.com'
    assert 'id' in data

def test_create_customer_missing_data(client, init_database):
    """Test creating customer with missing data."""
    response = client.post('/customers', json={'name': 'Bob'})
    assert response.status_code == 400
    assert 'Missing data' in response.get_json()['message']

def test_create_customer_duplicate_email(client, init_database):
    """Test creating customer with duplicate email."""
    # First, ensure a customer exists (from initial data or create one)
    # Initial data has 'john.doe@example.com'
    response = client.post('/customers', json={
        'name': 'John',
        'surname': 'Dorian',
        'email': 'john.doe@example.com' # Duplicate email
    })
    assert response.status_code == 409
    assert 'Customer with this email already exists' in response.get_json()['message']

def test_get_customers(client, init_database):
    """Test retrieving all customers."""
    response = client.get('/customers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Initial data adds 2 customers, this test might add more if run after others without clean db.
    # init_database fixture should handle DB cleaning per test or session.
    # If init_database is function-scoped and repopulates, we expect 2 from initial data.
    assert len(data) >= 2 # Should be exactly 2 if db is cleaned and repopulated by init_database fixture

def test_get_customer(client, init_database):
    """Test retrieving a single customer by ID."""
    # Assuming customer with ID 1 exists from initial data (John Doe)
    response = client.get('/customers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'John'

def test_get_customer_not_found(client, init_database):
    """Test retrieving a non-existent customer."""
    response = client.get('/customers/999')
    assert response.status_code == 404
    assert 'Customer not found' in response.get_json()['message']

def test_update_customer(client, init_database):
    """Test updating an existing customer."""
    # Assuming customer with ID 1 exists
    response = client.put('/customers/1', json={
        'name': 'Johnny',
        'surname': 'Doer',
        'email': 'johnny.doer@example.com'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Johnny'
    assert data['email'] == 'johnny.doer@example.com'

    # Verify update
    response_get = client.get('/customers/1')
    updated_data = response_get.get_json()
    assert updated_data['name'] == 'Johnny'

def test_update_customer_duplicate_email_on_update(client, init_database):
    """Test updating customer email to an existing one."""
    # Customer ID 1: john.doe@example.com
    # Customer ID 2: jane.smith@example.com
    # Try to update customer 1's email to customer 2's email
    response = client.put('/customers/1', json={'email': 'jane.smith@example.com'})
    assert response.status_code == 409
    assert 'Another customer with this email already exists' in response.get_json()['message']


def test_update_customer_not_found(client, init_database):
    """Test updating a non-existent customer."""
    response = client.put('/customers/999', json={'name': 'Ghost'})
    assert response.status_code == 404

def test_delete_customer(client, init_database):
    """Test deleting a customer."""
    # Create a customer to delete to avoid issues with FK constraints from orders on initial data
    res_create = client.post('/customers', json={
        'name': 'ToDelete',
        'surname': 'Person',
        'email': 'todelete@example.com'
    })
    assert res_create.status_code == 201
    customer_id_to_delete = res_create.get_json()['id']

    response_delete = client.delete(f'/customers/{customer_id_to_delete}')
    assert response_delete.status_code == 200
    assert 'Customer deleted' in response_delete.get_json()['message']

    # Verify customer is deleted
    response_get = client.get(f'/customers/{customer_id_to_delete}')
    assert response_get.status_code == 404

def test_delete_customer_not_found(client, init_database):
    """Test deleting a non-existent customer."""
    response = client.delete('/customers/999')
    assert response.status_code == 404
    assert 'Customer not found' in response.get_json()['message']

# Note on deleting customers with orders:
# The current Customer DELETE endpoint doesn't prevent deletion if orders exist.
# SQLAlchemy's default behavior with relationships might lead to FK constraint errors
# if the database enforces them and 'on delete' behavior isn't set (e.g., CASCADE).
# For SQLite, PRAGMA foreign_keys=ON must be active for FK enforcement.
# If the Order model's customer relationship had cascade="all, delete-orphan", orders would be deleted.
# Tests for this behavior would be more complex, involving creating orders first.
# For now, the delete test creates a new customer without orders.
# A test for deleting a customer with orders would look like:
# 1. Create customer
# 2. Create shop item
# 3. Create order for that customer with that item
# 4. Attempt to delete customer
# 5. Assert based on expected behavior (e.g., 409 if prevented, or 200 and check orders are also gone if cascaded)
# The `Customer.orders` relationship does not have `cascade="all, delete-orphan"` by default.
# The `Order.customer_id` FK does not have `ondelete="CASCADE"` by default in SQLAlchemy model for SQLite.
# So, deleting a customer with orders might fail if FKs are enforced and no cascade is set.
# Let's assume test default (SQLite in-memory) might not enforce FKs strictly unless explicitly configured.
# The `init_database` fixture uses `add_initial_data_for_tests` which creates customers and orders.
# Customer 1 (John Doe) has orders.
# Let's test deleting customer 1. The current customer delete route doesn't check for orders.
# It might fail if FK constraints are active and no cascade is defined.
# Or it might succeed, orphaning orders, or deleting them if default cascades apply at DB level.

def test_delete_customer_with_orders_behavior(client, init_database):
    """Test deleting a customer that has orders."""
    # Customer 1 (John Doe) from initial data has orders.
    # With cascade="all, delete-orphan" on Customer.orders (set in models.py),
    # deleting a customer should also delete their orders.

    # Check initial orders for customer 1
    orders_before_delete = client.get('/orders').get_json()
    customer1_orders_before = [o for o in orders_before_delete if o['customer_id'] == 1]
    assert len(customer1_orders_before) > 0, "Customer 1 should have orders from initial data for this test."

    response = client.delete('/customers/1')

    # Expect 200 OK as the deletion should succeed and cascade.
    assert response.status_code == 200, \
        f"Expected 200 OK when deleting customer with orders (cascade delete). Got {response.status_code}. Response: {response.data}"
    assert 'Customer deleted' in response.get_json()['message']

    # Verify customer is deleted
    get_cust_response = client.get('/customers/1')
    assert get_cust_response.status_code == 404, "Customer should be deleted."

    # Verify that orders associated with customer 1 are also deleted
    orders_after_delete = client.get('/orders').get_json()
    customer1_orders_after = [o for o in orders_after_delete if o['customer_id'] == 1]
    assert len(customer1_orders_after) == 0, \
        "Orders for customer 1 should have been cascade deleted, but some were found."
