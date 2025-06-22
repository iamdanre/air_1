import json
import pytest

# Initial data: item1='Laptop' (cat: Electronics), item2='Novel' (cat: Books), item3='T-Shirt' (cat: Clothing) etc.
# Cat IDs: Electronics:1, Books:2, Clothing:3

def test_create_item(client, init_database):
    response = client.post('/items', json={
        'title': 'New Gadget',
        'description': 'A cool new gadget.',
        'price': 99.99,
        'category_ids': [1] # Electronics category
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'New Gadget'
    assert data['price'] == 99.99
    assert len(data['categories']) == 1
    assert data['categories'][0]['id'] == 1

def test_create_item_multiple_categories(client, init_database):
    response = client.post('/items', json={
        'title': 'Versatile Item',
        'description': 'Usable in many ways.',
        'price': 49.50,
        'category_ids': [1, 3] # Electronics and Clothing
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Versatile Item'
    assert len(data['categories']) == 2
    cat_ids_in_response = sorted([cat['id'] for cat in data['categories']])
    assert cat_ids_in_response == [1, 3]


def test_create_item_no_categories(client, init_database):
    response = client.post('/items', json={
        'title': 'Uncategorized Item',
        'description': 'No specific category.',
        'price': 10.00
        # 'category_ids' is omitted or can be empty list
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Uncategorized Item'
    assert len(data['categories']) == 0

    response_empty_list = client.post('/items', json={
        'title': 'Uncategorized Item 2',
        'description': 'No specific category, empty list.',
        'price': 12.00,
        'category_ids': []
    })
    assert response_empty_list.status_code == 201
    data_empty_list = response_empty_list.get_json()
    assert data_empty_list['title'] == 'Uncategorized Item 2'
    assert len(data_empty_list['categories']) == 0


def test_create_item_invalid_category_id(client, init_database):
    response = client.post('/items', json={
        'title': 'Item with Bad Category',
        'price': 5.00,
        'category_ids': [999] # Non-existent category
    })
    assert response.status_code == 404 # Route returns 404 if a category_id is not found
    assert 'One or more categories not found' in response.get_json()['message']

def test_create_item_missing_title(client, init_database):
    response = client.post('/items', json={'price': 10.00})
    assert response.status_code == 400
    assert 'Missing title or price' in response.get_json()['message']

def test_create_item_missing_price(client, init_database):
    response = client.post('/items', json={'title': 'No Price Item'})
    assert response.status_code == 400
    assert 'Missing title or price' in response.get_json()['message']

def test_create_item_duplicate_title(client, init_database):
    # 'Laptop' item exists from initial data
    response = client.post('/items', json={'title': 'Laptop', 'price': 100.00})
    assert response.status_code == 409
    assert 'Item with this title already exists' in response.get_json()['message']

def test_get_items(client, init_database):
    response = client.get('/items')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 5 # 5 items from initial data

def test_get_item(client, init_database):
    # Item ID 1 is 'Laptop'
    response = client.get('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['title'] == 'Laptop'
    assert len(data['categories']) > 0 # Laptop is in Electronics

def test_get_item_not_found(client, init_database):
    response = client.get('/items/999')
    assert response.status_code == 404

def test_update_item(client, init_database):
    # Item ID 1 'Laptop'
    new_title = "Advanced Laptop Pro"
    new_price = 1500.75
    new_cat_ids = [1, 2] # Electronics, Books (e.g. programming book bundle)

    response = client.put('/items/1', json={
        'title': new_title,
        'price': new_price,
        'description': 'Updated description',
        'category_ids': new_cat_ids
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == new_title
    assert data['price'] == new_price
    assert data['description'] == 'Updated description'
    response_cat_ids = sorted([cat['id'] for cat in data['categories']])
    assert response_cat_ids == sorted(new_cat_ids)

    # Verify
    get_res = client.get('/items/1')
    updated_data = get_res.get_json()
    assert updated_data['title'] == new_title
    assert updated_data['price'] == new_price


def test_update_item_remove_categories(client, init_database):
    # Item ID 1 ('Laptop') initially has categories.
    # Update to have no categories.
    response = client.put('/items/1', json={'category_ids': []})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['categories']) == 0

    # Verify
    get_res = client.get('/items/1')
    updated_data = get_res.get_json()
    assert len(updated_data['categories']) == 0


def test_update_item_invalid_category_id(client, init_database):
    response = client.put('/items/1', json={'category_ids': [1, 999]}) # 999 is invalid
    assert response.status_code == 404
    assert 'One or more categories not found: [999]' in response.get_json()['message']

def test_update_item_duplicate_title(client, init_database):
    # Item 1: Laptop, Item 2: Novel - The Great Gatsby
    # Try to update item 1's title to item 2's title
    response = client.put('/items/1', json={'title': 'Novel - The Great Gatsby'})
    assert response.status_code == 409

def test_update_item_not_found(client, init_database):
    response = client.put('/items/999', json={'title': 'Ghost Item'})
    assert response.status_code == 404

def test_delete_item(client, init_database):
    # Create a new item to delete to avoid issues with existing orders
    res_create = client.post('/items', json={
        'title': 'Temporary Item',
        'price': 1.00,
        'category_ids': []
    })
    assert res_create.status_code == 201
    item_id_to_delete = res_create.get_json()['id']

    response_delete = client.delete(f'/items/{item_id_to_delete}')
    assert response_delete.status_code == 200
    assert 'Item deleted' in response_delete.get_json()['message']

    # Verify deleted
    get_res = client.get(f'/items/{item_id_to_delete}')
    assert get_res.status_code == 404

def test_delete_item_not_found(client, init_database):
    response = client.delete('/items/999')
    assert response.status_code == 404

def test_delete_item_in_order(client, init_database):
    # Item 1 ('Laptop') is part of initial orders.
    response = client.delete('/items/1')
    assert response.status_code == 409 # As per current route logic
    assert 'Cannot delete item as it is part of existing orders' in response.get_json()['message']

    # Verify item was not deleted
    get_res = client.get('/items/1')
    assert get_res.status_code == 200
    assert get_res.get_json()['title'] == 'Laptop'
