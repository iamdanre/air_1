from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for the many-to-many relationship between ShopItem and ShopItemCategory
item_categories_table = db.Table('item_categories',
    db.Column('shop_item_id', db.Integer, db.ForeignKey('shop_item.id'), primary_key=True),
    db.Column('shop_item_category_id', db.Integer, db.ForeignKey('shop_item_category.id'), primary_key=True)
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }

class ShopItemCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

class ShopItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    categories = db.relationship('ShopItemCategory', secondary=item_categories_table,
                                 lazy='subquery', backref=db.backref('shop_items', lazy=True))
    order_items = db.relationship('OrderItem', backref='shop_item_obj', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'categories': [category.to_dict() for category in self.categories]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_item_id = db.Column(db.Integer, db.ForeignKey('shop_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    # shop_item relationship is defined by backref from ShopItem.order_items as shop_item_obj

    def to_dict(self):
        data = {
            'id': self.id,
            'shop_item_id': self.shop_item_id,
            'quantity': self.quantity,
            'order_id': self.order_id
        }
        if self.shop_item_obj: # shop_item_obj is the backref from ShopItem
            data['shop_item'] = self.shop_item_obj.to_dict() # Be careful with recursion if ShopItem includes OrderItems
        return data


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    # customer relationship is defined by backref from Customer.orders

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'items': [item.to_dict() for item in self.items]
        }
