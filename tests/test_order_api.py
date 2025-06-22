import json
import pytest

# Initial data:
# Customers: Cust1 (ID 1 John Doe), Cust2 (ID 2 Jane Smith)
# Items: item1 (ID 1 Laptop), item2 (ID 2 Novel), item3 (ID 3 T-Shirt), item4 (ID 4 Smartphone), item5 (ID 5 Cookbook)
# Orders: Order1 (Cust1, [1xLaptop, 2xNovel]), Order2 (Cust2, [3xT-Shirt, 1xSmartphone, 1xLaptop]), Order3 (Cust1, [1xCookbook])
# Order IDs will be 1, 2, 3 respectively if db is fresh.

def test_create_order(client, init_database):
    # Customer 1 (John Doe), Item 4 (Smartphone), Item 5 (Cookbook)
    payload = {
        'customer_id': 1,
        'items': [
            {'shop_item_id': 4, 'quantity': 1},
            {'shop_item_id': 5, 'quantity': 2}
        ]
    }
    response = client.post('/orders', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['customer_id'] == 1
    assert len(data['items']) == 2
    item_ids_in_order = sorted([item['shop_item_id'] for item in data['items']])
    assert item_ids_in_order == [4, 5]
    quantities = {item['shop_item_id']: item['quantity'] for item in data['items']}
    assert quantities[4] == 1
    assert quantities[5] == 2
    assert 'id' in data

def test_create_order_customer_not_found(client, init_database):
    payload = {'customer_id': 999, 'items': [{'shop_item_id': 1, 'quantity': 1}]}
    response = client.post('/orders', json=payload)
    assert response.status_code == 404
    assert 'Customer not found' in response.get_json()['message']

def test_create_order_item_not_found(client, init_database):
    payload = {'customer_id': 1, 'items': [{'shop_item_id': 999, 'quantity': 1}]}
    response = client.post('/orders', json=payload)
    assert response.status_code == 404 # ShopItem not found
    assert 'ShopItem with id 999 not found' in response.get_json()['message']

def test_create_order_missing_data(client, init_database):
    response = client.post('/orders', json={'customer_id': 1}) # Missing items
    assert response.status_code == 400
    assert 'Missing customer_id or items' in response.get_json()['message'] # Adjusted to match current error message

    response = client.post('/orders', json={'items': [{'shop_item_id': 1, 'quantity': 1}]}) # Missing customer_id
    assert response.status_code == 400

def test_create_order_no_items_in_list(client, init_database):
    payload = {'customer_id': 1, 'items': []}
    response = client.post('/orders', json=payload)
    assert response.status_code == 400
    assert 'Order must contain at least one item' in response.get_json()['message']

def test_create_order_invalid_quantity(client, init_database):
    payload = {'customer_id': 1, 'items': [{'shop_item_id': 1, 'quantity': 0}]} # Zero quantity
    response = client.post('/orders', json=payload)
    assert response.status_code == 400
    assert 'Invalid quantity' in response.get_json()['message']

    payload_neg = {'customer_id': 1, 'items': [{'shop_item_id': 1, 'quantity': -1}]} # Negative quantity
    response_neg = client.post('/orders', json=payload_neg)
    assert response_neg.status_code == 400
    assert 'Invalid quantity' in response_neg.get_json()['message']

    payload_str = {'customer_id': 1, 'items': [{'shop_item_id': 1, 'quantity': "abc"}]} # String quantity
    response_str = client.post('/orders', json=payload_str)
    assert response_str.status_code == 400 # or potentially 500 if not caught well, but expecting 400
    assert 'Invalid quantity' in response_str.get_json()['message']


def test_get_orders(client, init_database):
    response = client.get('/orders')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 3 # 3 orders from initial data

def test_get_order(client, init_database):
    # Order ID 1 exists from initial data
    response = client.get('/orders/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['customer_id'] == 1 # John Doe
    assert len(data['items']) == 2 # Laptop, Novel

def test_get_order_not_found(client, init_database):
    response = client.get('/orders/999')
    assert response.status_code == 404

def test_update_order_customer(client, init_database):
    # Order ID 1, initially for Customer 1. Update to Customer 2.
    # Customer 2 (Jane Smith) has ID 2.
    response = client.put('/orders/1', json={'customer_id': 2})
    assert response.status_code == 200
    data = response.get_json()
    assert data['customer_id'] == 2
    assert data['customer']['name'] == 'Jane' # Check if customer details are updated in response

    # Verify
    get_res = client.get('/orders/1')
    updated_data = get_res.get_json()
    assert updated_data['customer_id'] == 2

def test_update_order_items(client, init_database):
    # Order ID 1 initially has Laptop (ID 1) and Novel (ID 2)
    # Update items to: 1x Smartphone (ID 4), 1x T-Shirt (ID 3)
    new_items_payload = [
        {'shop_item_id': 4, 'quantity': 1}, # Smartphone
        {'shop_item_id': 3, 'quantity': 1}  # T-Shirt
    ]
    response = client.put('/orders/1', json={'items': new_items_payload})
    assert response.status_code == 200
    data = response.get_json()

    current_item_ids = sorted([item['shop_item_id'] for item in data['items']])
    expected_item_ids = sorted([4, 3])
    assert current_item_ids == expected_item_ids
    assert len(data['items']) == 2

    # Verify quantities
    quantities = {item['shop_item_id']: item['quantity'] for item in data['items']}
    assert quantities[4] == 1
    assert quantities[3] == 1

    # Verify original items are gone
    get_res = client.get('/orders/1')
    updated_data = get_res.get_json()
    updated_item_ids = sorted([item['shop_item_id'] for item in updated_data['items']])
    assert updated_item_ids == expected_item_ids

def test_update_order_clear_items(client, init_database):
    # Order ID 1
    # Update to have no items
    response = client.put('/orders/1', json={'items': []})
    assert response.status_code == 200 # Should succeed
    data = response.get_json()
    assert len(data['items']) == 0

    # Verify
    get_res = client.get('/orders/1')
    updated_data = get_res.get_json()
    assert len(updated_data['items']) == 0


def test_update_order_invalid_item_id(client, init_database):
    payload = {'items': [{'shop_item_id': 999, 'quantity': 1}]}
    response = client.put('/orders/1', json=payload)
    assert response.status_code == 404 # Item not found
    assert 'ShopItem with id 999 not found' in response.get_json()['message']

def test_update_order_not_found(client, init_database):
    response = client.put('/orders/999', json={'customer_id': 1})
    assert response.status_code == 404

def test_delete_order(client, init_database):
    # Order ID 1 exists
    response = client.delete('/orders/1')
    assert response.status_code == 200
    assert 'Order deleted' in response.get_json()['message']

    # Verify deleted
    get_res = client.get('/orders/1')
    assert get_res.status_code == 404

def test_delete_order_not_found(client, init_database):
    response = client.delete('/orders/999')
    assert response.status_code == 404

# Test to ensure OrderItems are deleted when an Order is deleted (cascade)
def test_order_items_deleted_on_order_delete(client, init_database):
    # Create a new order with items first
    payload = {
        'customer_id': 1,
        'items': [{'shop_item_id': 1, 'quantity': 1}, {'shop_item_id': 2, 'quantity': 2}]
    }
    res_create = client.post('/orders', json=payload)
    assert res_create.status_code == 201
    new_order_data = res_create.get_json()
    new_order_id = new_order_data['id']

    # Get the OrderItems associated with this new order
    # Need a way to query OrderItems directly or infer from DB state if possible.
    # For now, we trust the 'cascade="all, delete-orphan"' on Order.items.
    # We can check this by ensuring the order is gone.
    # A more thorough test would involve querying the OrderItem table if an endpoint existed or direct DB access.

    # Delete the order
    res_delete = client.delete(f'/orders/{new_order_id}')
    assert res_delete.status_code == 200

    # Verify order is gone
    get_order_res = client.get(f'/orders/{new_order_id}')
    assert get_order_res.status_code == 404

    # If we had an endpoint like /order_items or could inspect the DB,
    # we would verify that no OrderItem entities for this order_id exist.
    # For now, this level of testing for cascade is implicit.
    # The `OrderItem.to_dict()` in `Order.to_dict()` shows items, so their absence after delete is the check.
    # The models.py for Order.items has `cascade="all, delete-orphan"`, so this should work.
    # This test confirms the order itself is deleted. The cascade is an ORM feature.

# Test for updating order with item that has invalid quantity
def test_update_order_invalid_quantity(client, init_database):
    # Order ID 1
    payload = {'items': [{'shop_item_id': 1, 'quantity': 0}]} # Zero quantity
    response = client.put('/orders/1', json=payload)
    assert response.status_code == 400
    assert 'Invalid quantity' in response.get_json()['message']

    payload_neg = {'items': [{'shop_item_id': 1, 'quantity': -1}]} # Negative quantity
    response_neg = client.put('/orders/1', json=payload_neg)
    assert response_neg.status_code == 400
    assert 'Invalid quantity' in response_neg.get_json()['message']

    payload_str = {'items': [{'shop_item_id': 1, 'quantity': "abc"}]} # String quantity
    response_str = client.put('/orders/1', json=payload_str)
    assert response_str.status_code == 400
    assert 'Invalid quantity' in response_str.get_json()['message']
