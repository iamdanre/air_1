from app import create_app
import os

# Create the Flask app instance using the factory function
# We are not in testing mode when running `run.py` directly
app = create_app(testing=False)

if __name__ == '__main__':
    # The host '0.0.0.0' makes the server publicly available (or available on the local network)
    # Debug should be False in a production environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
