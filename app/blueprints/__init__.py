"""
Blueprints package initialization
This package contains all the blueprints for organizing API routes

Available blueprints:
- customer: Customer management endpoints
- mechanic: Mechanic management endpoints
- service_ticket: Service ticket management endpoints
- inventory: Inventory management endpoints
"""

# Import all blueprints for easy access
from app.blueprints.customer import customer_bp
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.service_ticket import service_ticket_bp
from app.blueprints.inventory import inventory_bp

# Export all blueprints for external import
__all__ = [
    'customer_bp',
    'mechanic_bp',
    'service_ticket_bp',
    'inventory_bp'
]