from flask import Blueprint

# Create mechanic blueprint
mechanic_bp = Blueprint('mechanic', __name__)

# Import routes to register them with the blueprint
from app.blueprints.mechanic import routes
