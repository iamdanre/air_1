from sqlalchemy.orm import Session
from models import Customer, ShopItemCategory, ShopItem, Order, OrderItem
from schemas import CustomerCreate, ShopItemCategoryCreate, ShopItemCreate, OrderCreate

# --- Customer CRUD ---
def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        for k, v in customer.dict().items():
            setattr(db_customer, k, v)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# --- ShopItemCategory CRUD ---
def get_categories(db: Session):
    return db.query(ShopItemCategory).all()

def get_category(db: Session, category_id: int):
    return db.query(ShopItemCategory).filter(ShopItemCategory.id == category_id).first()

def create_category(db: Session, category: ShopItemCategoryCreate):
    db_category = ShopItemCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: ShopItemCategoryCreate):
    db_category = get_category(db, category_id)
    if db_category:
        for k, v in category.dict().items():
            setattr(db_category, k, v)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# --- ShopItem CRUD ---
def get_items(db: Session):
    return db.query(ShopItem).all()

def get_item(db: Session, item_id: int):
    return db.query(ShopItem).filter(ShopItem.id == item_id).first()

def create_item(db: Session, item: ShopItemCreate):
    categories = db.query(ShopItemCategory).filter(ShopItemCategory.id.in_(item.category_ids)).all()
    db_item = ShopItem(title=item.title, description=item.description, price=item.price, categories=categories)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ShopItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        for k, v in item.dict(exclude={'category_ids'}).items():
            setattr(db_item, k, v)
        db_item.categories = db.query(ShopItemCategory).filter(ShopItemCategory.id.in_(item.category_ids)).all()
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- Order CRUD ---
def get_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def create_order(db: Session, order: OrderCreate):
    db_order = Order(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()
    for item in order.items:
        db_item = OrderItem(order_id=db_order.id, shopitem_id=item.shopitem_id, quantity=item.quantity)
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: OrderCreate):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.customer_id = order.customer_id
        db.query(OrderItem).filter(OrderItem.order_id == db_order.id).delete()
        for item in order.items:
            db_item = OrderItem(order_id=db_order.id, shopitem_id=item.shopitem_id, quantity=item.quantity)
            db.add(db_item)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order 