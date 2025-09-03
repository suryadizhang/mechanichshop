from flask import Blueprint

# Create service_ticket blueprint
service_ticket_bp = Blueprint('service_ticket', __name__)

# Import routes to register them with the blueprint
from app.blueprints.service_ticket import routes
