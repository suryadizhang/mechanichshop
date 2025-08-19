import os
from app import create_app
from app.extention import db
from app.models import Customer, Mechanic, ServiceTicket, Inventory

# Get environment from environment variable (defaults to development)
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app using factory pattern 
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """
    This makes the models available when we run flask shell
    Pretty convenient for testing stuff
    """
    return {
        'db': db,
        'Customer': Customer,
        'Mechanic': Mechanic,
        'ServiceTicket': ServiceTicket,
        'Inventory': Inventory  # Added inventory model
    }

@app.route('/')
def index():
    """Basic index route - just shows API info"""
    return {
        'message': 'Welcome to Mechanic Shop API',
        'version': '1.0.0',
        'status': 'Running',
        'endpoints': {
            'customers': '/customers',
            'mechanics': '/mechanics', 
            'service_tickets': '/service-tickets',
            'inventory': '/inventory'  # Added this after implementing inventory
        }
    }

if __name__ == '__main__':
    # Create database tables first
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    
    # Run the development server
    app.run(debug=True, host='0.0.0.0', port=5000)


