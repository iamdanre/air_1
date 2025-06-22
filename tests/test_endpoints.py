import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Customer Tests ---
def test_create_and_get_customer():
    resp = client.post('/customers', json={"name": "Test", "surname": "User", "email": "testuser@example.com"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test"
    customer_id = data["id"]
    resp = client.get(f'/customers/{customer_id}')
    assert resp.status_code == 200
    assert resp.json()["email"] == "testuser@example.com"

def test_update_customer():
    resp = client.post('/customers', json={"name": "Update", "surname": "Me", "email": "updateme@example.com"})
    customer_id = resp.json()["id"]
    resp = client.put(f'/customers/{customer_id}', json={"name": "Updated", "surname": "Me", "email": "updateme@example.com"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"

def test_delete_customer():
    resp = client.post('/customers', json={"name": "Delete", "surname": "Me", "email": "deleteme@example.com"})
    customer_id = resp.json()["id"]
    resp = client.delete(f'/customers/{customer_id}')
    assert resp.status_code == 200
    resp = client.get(f'/customers/{customer_id}')
    assert resp.status_code == 404

# --- Category Tests ---
def test_create_and_get_category():
    resp = client.post('/categories', json={"title": "Toys", "description": "Fun stuff"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Toys"
    category_id = data["id"]
    resp = client.get(f'/categories/{category_id}')
    assert resp.status_code == 200
    assert resp.json()["description"] == "Fun stuff"

def test_update_category():
    resp = client.post('/categories', json={"title": "Old", "description": "Old desc"})
    category_id = resp.json()["id"]
    resp = client.put(f'/categories/{category_id}', json={"title": "New", "description": "New desc"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"

def test_delete_category():
    resp = client.post('/categories', json={"title": "DeleteCat", "description": "To delete"})
    category_id = resp.json()["id"]
    resp = client.delete(f'/categories/{category_id}')
    assert resp.status_code == 200
    resp = client.get(f'/categories/{category_id}')
    assert resp.status_code == 404

# --- ShopItem Tests ---
def test_create_and_get_item():
    # Create a category first
    cat_resp = client.post('/categories', json={"title": "Books2", "description": "Books desc"})
    cat_id = cat_resp.json()["id"]
    resp = client.post('/items', json={"title": "BookX", "description": "A book", "price": 10.0, "category_ids": [cat_id]})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "BookX"
    item_id = data["id"]
    resp = client.get(f'/items/{item_id}')
    assert resp.status_code == 200
    assert resp.json()["description"] == "A book"

def test_update_item():
    cat_resp = client.post('/categories', json={"title": "CatA", "description": "desc"})
    cat_id = cat_resp.json()["id"]
    resp = client.post('/items', json={"title": "ItemA", "description": "desc", "price": 5.0, "category_ids": [cat_id]})
    item_id = resp.json()["id"]
    resp = client.put(f'/items/{item_id}', json={"title": "ItemB", "description": "desc2", "price": 6.0, "category_ids": [cat_id]})
    assert resp.status_code == 200
    assert resp.json()["title"] == "ItemB"

def test_delete_item():
    cat_resp = client.post('/categories', json={"title": "CatB", "description": "desc"})
    cat_id = cat_resp.json()["id"]
    resp = client.post('/items', json={"title": "ItemDel", "description": "desc", "price": 5.0, "category_ids": [cat_id]})
    item_id = resp.json()["id"]
    resp = client.delete(f'/items/{item_id}')
    assert resp.status_code == 200
    resp = client.get(f'/items/{item_id}')
    assert resp.status_code == 404

# --- Order Tests ---
def test_create_and_get_order():
    cust_resp = client.post('/customers', json={"name": "Order", "surname": "User", "email": "orderuser@example.com"})
    cust_id = cust_resp.json()["id"]
    cat_resp = client.post('/categories', json={"title": "OrderCat", "description": "desc"})
    cat_id = cat_resp.json()["id"]
    item_resp = client.post('/items', json={"title": "OrderItem", "description": "desc", "price": 20.0, "category_ids": [cat_id]})
    item_id = item_resp.json()["id"]
    order_resp = client.post('/orders', json={"customer_id": cust_id, "items": [{"shopitem_id": item_id, "quantity": 3}]})
    assert order_resp.status_code == 200
    order_id = order_resp.json()["id"]
    get_resp = client.get(f'/orders/{order_id}')
    assert get_resp.status_code == 200
    assert get_resp.json()["customer"]["id"] == cust_id

def test_update_order():
    cust_resp = client.post('/customers', json={"name": "Order2", "surname": "User2", "email": "orderuser2@example.com"})
    cust_id = cust_resp.json()["id"]
    cat_resp = client.post('/categories', json={"title": "OrderCat2", "description": "desc"})
    cat_id = cat_resp.json()["id"]
    item_resp = client.post('/items', json={"title": "OrderItem2", "description": "desc", "price": 30.0, "category_ids": [cat_id]})
    item_id = item_resp.json()["id"]
    order_resp = client.post('/orders', json={"customer_id": cust_id, "items": [{"shopitem_id": item_id, "quantity": 1}]})
    order_id = order_resp.json()["id"]
    # Update order
    order_resp = client.put(f'/orders/{order_id}', json={"customer_id": cust_id, "items": [{"shopitem_id": item_id, "quantity": 2}]})
    assert order_resp.status_code == 200
    assert order_resp.json()["items"][0]["quantity"] == 2

def test_delete_order():
    cust_resp = client.post('/customers', json={"name": "Order3", "surname": "User3", "email": "orderuser3@example.com"})
    cust_id = cust_resp.json()["id"]
    cat_resp = client.post('/categories', json={"title": "OrderCat3", "description": "desc"})
    cat_id = cat_resp.json()["id"]
    item_resp = client.post('/items', json={"title": "OrderItem3", "description": "desc", "price": 40.0, "category_ids": [cat_id]})
    item_id = item_resp.json()["id"]
    order_resp = client.post('/orders', json={"customer_id": cust_id, "items": [{"shopitem_id": item_id, "quantity": 1}]})
    order_id = order_resp.json()["id"]
    del_resp = client.delete(f'/orders/{order_id}')
    assert del_resp.status_code == 200
    get_resp = client.get(f'/orders/{order_id}')
    assert get_resp.status_code == 404 