from flask import Blueprint

# Create customer blueprint
customer_bp = Blueprint('customer', __name__)

# Import routes to register them with the blueprint
from app.blueprints.customer import routes
