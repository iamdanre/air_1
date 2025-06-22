import pytest
from app import create_app
from app.models.models import db
from app.utils.db_utils import add_initial_data as add_initial_data_util # Renamed to avoid conflict

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Setup: create app with testing config
    flask_app = create_app(testing=True)

    # Establish an application context before running the tests.
    with flask_app.app_context():
        db.create_all() # Create tables for the in-memory database
        # If you need initial data for all tests, you can add it here.
        # add_initial_test_data(flask_app) # Example: a function to add test-specific initial data
        # For this project, we'll have tests add their own specific data or use the utility if general data is needed.

    yield flask_app

    # Teardown: (not strictly necessary for in-memory SQLite as it's recreated, but good practice)
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function') # Changed to function scope for data isolation between tests
def init_database(app):
    """Clear and initialize database with fresh test data for each test function."""
    with app.app_context():
        db.drop_all() # Clear existing data
        db.create_all() # Create tables
        add_initial_data_for_tests(app) # Add a consistent set of data for tests
        # print("Test database initialized and populated.") # For debugging
    yield db # Can be used by tests to make further db manipulations if needed
    # Teardown can be done here if needed, but drop_all() at start of next use is also fine

def add_initial_data_for_tests(flask_app):
    """Adds a consistent set of initial data for testing purposes."""
    # This function is similar to add_initial_data but tailored for tests.
    # It ensures tests run against a known state.
    # It's called by the init_database fixture.
    with flask_app.app_context():
        # Using the same utility function for now, ensure it's suitable for test scenarios
        # or create a separate one for test data.
        add_initial_data_util(flask_app)
        # print("Initial data added for tests.") # For debugging

# Example of how a test might use init_database:
# def test_example(client, init_database):
#     response = client.get('/customers')
#     assert response.status_code == 200
#     # assertions on data that was populated by init_database
#     # ...

# Note: If add_initial_data_util checks if data exists and skips,
# for tests, we need it to run every time init_database is called.
# So, the check inside add_initial_data_util might need adjustment or
# we ensure db.drop_all() is effective.
# The current add_initial_data has a check:
# if Customer.query.first() is not None: print("Data already exists. Skipping initial data population.")
# This is fine because init_database does a drop_all() first.
