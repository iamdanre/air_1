from app.models.models import db, Customer, ShopItemCategory, ShopItem, OrderItem, Order

def init_db(app):
    """Initializes the database and creates tables."""
    with app.app_context():
        db.create_all()
    print("Database tables created.")

def add_initial_data(app):
    """Adds initial test data to the database."""
    with app.app_context():
        # Check if data already exists to prevent duplicates
        if Customer.query.first() is not None:
            print("Data already exists. Skipping initial data population.")
            return

        # Create Categories
        cat1 = ShopItemCategory(title='Electronics', description='Gadgets and devices')
        cat2 = ShopItemCategory(title='Books', description='Various genres of books')
        cat3 = ShopItemCategory(title='Clothing', description='Men and Women apparel')
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()
        print("Added categories.")

        # Create ShopItems
        item1 = ShopItem(title='Laptop', description='High-performance laptop', price=1200.00, categories=[cat1])
        item2 = ShopItem(title='Novel - The Great Gatsby', description='A classic novel', price=15.99, categories=[cat2])
        item3 = ShopItem(title='T-Shirt', description='Cotton T-Shirt', price=25.50, categories=[cat3])
        item4 = ShopItem(title='Smartphone', description='Latest model smartphone', price=800.00, categories=[cat1])
        item5 = ShopItem(title='Cookbook', description='Recipes for everyone', price=30.00, categories=[cat2, cat3]) # Item in multiple categories
        db.session.add_all([item1, item2, item3, item4, item5])
        db.session.commit()
        print("Added shop items.")

        # Create Customers
        cust1 = Customer(name='John', surname='Doe', email='john.doe@example.com')
        cust2 = Customer(name='Jane', surname='Smith', email='jane.smith@example.com')
        db.session.add_all([cust1, cust2])
        db.session.commit()
        print("Added customers.")

        # Create Orders
        # Order 1 for John Doe
        order1_item1 = OrderItem(shop_item_obj=item1, quantity=1)
        order1_item2 = OrderItem(shop_item_obj=item2, quantity=2)
        order1 = Order(customer=cust1, items=[order1_item1, order1_item2])

        # Order 2 for Jane Smith
        order2_item1 = OrderItem(shop_item_obj=item3, quantity=3)
        order2_item2 = OrderItem(shop_item_obj=item4, quantity=1)
        order2_item3 = OrderItem(shop_item_obj=item1, quantity=1) # Jane also buys a laptop
        order2 = Order(customer=cust2, items=[order2_item1, order2_item2, order2_item3])

        # Order 3 for John Doe (another order)
        order3_item1 = OrderItem(shop_item_obj=item5, quantity=1)
        order3 = Order(customer=cust1, items=[order3_item1])

        db.session.add_all([order1, order2, order3])
        db.session.commit()
        print("Added orders with items.")

        print("Initial data added to the database.")
