from flask import Flask
from app.models.models import db
from app.utils.db_utils import init_db, add_initial_data
import os

def create_app(testing=False):
    app = Flask(__name__)

    # Configure the database URI
    # Use an in-memory SQLite database for testing, otherwise use a file-based one.
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        # Ensure the instance folder exists for the SQLite file
        instance_path = os.path.join(app.instance_path)
        if not os.path.exists(instance_path):
            try:
                os.makedirs(instance_path)
            except OSError as e:
                # Handle error if instance path cannot be created, e.g., permissions
                print(f"Error creating instance path {instance_path}: {e}")
                # Fallback or raise might be needed depending on desired behavior

        db_path = os.path.join(instance_path, 'shop.sqlite')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register blueprints
    from app.routes.customer_routes import customer_bp
    from app.routes.category_routes import category_bp
    from app.routes.item_routes import item_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(order_bp)

    with app.app_context():
        # Create database tables if they don't exist
        # db.create_all() # Moved to init_db for more explicit control
        init_db(app) # Creates tables
        if not testing: # Don't add initial data if testing, tests should set up their own data
            add_initial_data(app) # Populates with initial data

    return app
