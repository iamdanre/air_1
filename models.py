from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for ShopItem and ShopItemCategory (many-to-many)
shopitem_category = Table(
    'shopitem_category', Base.metadata,
    Column('shopitem_id', Integer, ForeignKey('shop_items.id')),
    Column('category_id', Integer, ForeignKey('shop_item_categories.id'))
)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='customer')

class ShopItemCategory(Base):
    __tablename__ = 'shop_item_categories'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    items = relationship('ShopItem', secondary=shopitem_category, back_populates='categories')

class ShopItem(Base):
    __tablename__ = 'shop_items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    categories = relationship('ShopItemCategory', secondary=shopitem_category, back_populates='items')
    order_items = relationship('OrderItem', back_populates='shop_item')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    shopitem_id = Column(Integer, ForeignKey('shop_items.id'))
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    shop_item = relationship('ShopItem', back_populates='order_items')
    order = relationship('Order', back_populates='items')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan') 