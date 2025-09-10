import os
from app import create_app
from app.extention import db
from app.models import Customer, Mechanic, ServiceTicket, Inventory
from flask import jsonify
from datetime import datetime

# Load environment variables from .env file (only in development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not available (production environment)
    pass

# Get environment from environment variable (defaults to development)
config_name = os.environ.get("FLASK_ENV", "development")

# Create the Flask app using factory pattern
app = create_app(config_name)

# Expose app for Gunicorn
application = app


@app.shell_context_processor
def make_shell_context():
    """
    This makes the models available when we run flask shell
    Pretty convenient for testing stuff
    """
    return {
        "db": db,
        "Customer": Customer,
        "Mechanic": Mechanic,
        "ServiceTicket": ServiceTicket,
        "Inventory": Inventory,  # Added inventory model
    }


@app.route("/")
def index():
    """Basic index route - just shows API info"""
    return {
        "message": "Welcome to Mechanic Shop API",
        "version": "1.0.0",
        "status": "Running",
        "endpoints": {
            "customers": "/customers",
            "mechanics": "/mechanics",
            "service_tickets": "/service-tickets",
            "inventory": "/inventory",  # Added after implementing inventory
        },
    }


@app.route("/health", methods=["GET"])
def health_check():
    """API Health Check endpoint"""
    return (
        jsonify(
            {
                "status": "healthy",
                "message": "API is running successfully",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
            }
        ),
        200,
    )


@app.route("/info", methods=["GET"])
def api_info():
    """API Information endpoint"""
    return (
        jsonify(
            {
                "name": "Mechanic Shop API",
                "version": "1.0.0",
                "description": "A comprehensive API for managing mechanic "
                + "shop operations",
                "endpoints": {
                    "customers": "/customers",
                    "mechanics": "/mechanics",
                    "service_tickets": "/service-tickets",
                    "inventory": "/inventory",
                    "health": "/health",
                    "info": "/info",
                },
                "documentation": "/api/docs",
                "status": "operational",
            }
        ),
        200,
    )


if __name__ == "__main__":
    # Create database tables first
    with app.app_context():
        db.create_all()
        print("Database tables created!")

    # Run the development server only in development
    if config_name == "development":
        app.run(debug=True, host="0.0.0.0", port=5000)
