from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from typing import List

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Customer Endpoints ---
@app.get('/customers', response_model=List[schemas.Customer])
def read_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.get('/customers/{customer_id}', response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    return db_customer

@app.post('/customers', response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.put('/customers/{customer_id}', response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, customer)
    if not db_customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    return db_customer

@app.delete('/customers/{customer_id}', response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    return db_customer

# --- ShopItemCategory Endpoints ---
@app.get('/categories', response_model=List[schemas.ShopItemCategory])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.get('/categories/{category_id}', response_model=schemas.ShopItemCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    return db_category

@app.post('/categories', response_model=schemas.ShopItemCategory)
def create_category(category: schemas.ShopItemCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.put('/categories/{category_id}', response_model=schemas.ShopItemCategory)
def update_category(category_id: int, category: schemas.ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    return db_category

@app.delete('/categories/{category_id}', response_model=schemas.ShopItemCategory)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='Category not found')
    return db_category

# --- ShopItem Endpoints ---
@app.get('/items', response_model=List[schemas.ShopItem])
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get('/items/{item_id}', response_model=schemas.ShopItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_item

@app.post('/items', response_model=schemas.ShopItem)
def create_item(item: schemas.ShopItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.put('/items/{item_id}', response_model=schemas.ShopItem)
def update_item(item_id: int, item: schemas.ShopItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_item

@app.delete('/items/{item_id}', response_model=schemas.ShopItem)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return db_item

# --- Order Endpoints ---
@app.get('/orders', response_model=List[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.get('/orders/{order_id}', response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail='Order not found')
    return db_order

@app.post('/orders', response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.put('/orders/{order_id}', response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id, order)
    if not db_order:
        raise HTTPException(status_code=404, detail='Order not found')
    return db_order

@app.delete('/orders/{order_id}', response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail='Order not found')
    return db_order 