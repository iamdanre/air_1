from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, ShopItemCategory, ShopItem, Order, OrderItem
import os

SQLALCHEMY_DATABASE_URL = 'sqlite:///./shop.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    if not os.path.exists('./shop.db'):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        # Add test data
        c1 = Customer(name='Alice', surname='Smith', email='alice@example.com')
        c2 = Customer(name='Bob', surname='Brown', email='bob@example.com')
        cat1 = ShopItemCategory(title='Books', description='All kinds of books')
        cat2 = ShopItemCategory(title='Electronics', description='Gadgets and devices')
        item1 = ShopItem(title='Python 101', description='Learn Python', price=29.99, categories=[cat1])
        item2 = ShopItem(title='Laptop', description='A fast laptop', price=999.99, categories=[cat2])
        db.add_all([c1, c2, cat1, cat2, item1, item2])
        db.commit()
        order_item1 = OrderItem(shop_item=item1, quantity=2)
        order_item2 = OrderItem(shop_item=item2, quantity=1)
        order1 = Order(customer=c1, items=[order_item1, order_item2])
        db.add(order1)
        db.commit()
        db.close()

init_db() 