from flask import Blueprint

# Create inventory blueprint with URL prefix
inventory_bp = Blueprint('inventory', __name__)

# Import routes to register them with the blueprint
from app.blueprints.inventory import routes
