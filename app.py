"""
Application entry point
Creates and runs the Flask application using the Application Factory Pattern
"""
import os
from app import create_app
from app.extention import db
from app.models import Customer, Mechanic, ServiceTicket

# Get environment from environment variable or default to development
config_name = os.environ.get('FLASK_ENV', 'development')

# Create application instance using factory pattern
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """
    Shell context processor for Flask shell
    Makes database and models available in flask shell
    """
    return {
        'db': db,
        'Customer': Customer,
        'Mechanic': Mechanic,
        'ServiceTicket': ServiceTicket
    }

@app.route('/')
def index():
    """Basic index route"""
    return {
        'message': 'Welcome to Mechanic Shop API',
        'version': '1.0.0',
        'endpoints': {
            'customers': '/customers',
            'mechanics': '/mechanics',
            'service_tickets': '/service-tickets'
        }
    }

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)