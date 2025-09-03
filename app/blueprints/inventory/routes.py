"""
Inventory management routes
This was the new requirement - adding parts/inventory tracking
"""
from flask import request, jsonify
from app.blueprints.inventory import inventory_bp
from app.models import Inventory
from app.blueprints.inventory.schema import inventory_schema, inventories_schema
from app.extention import db, limiter, cache
from app.auth import mechanic_token_required


@inventory_bp.route('/', methods=['POST'])
@mechanic_token_required  # Only mechanics can add inventory (assignment requirement)
def create_inventory(current_mechanic_id):
    """POST '/': Creates a new Inventory item (mechanic only)"""
    # Mechanics manage the parts inventory
    try:
        inventory_data = inventory_schema.load(request.json)
        db.session.add(inventory_data)
        db.session.commit()
        # Cache will expire automatically after 5 minutes
        return inventory_schema.jsonify(inventory_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@inventory_bp.route('/', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes - assignment requirement
def get_inventories():
    """GET '/': Retrieves all Inventory items"""
    # Anyone can view inventory - no auth needed
    inventories = Inventory.query.all()
    return inventories_schema.jsonify(inventories), 200


@inventory_bp.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=300)  # Cache individual items too
def get_inventory(id):
    """GET '/<int:id>': Retrieves a specific Inventory item"""
    inventory = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route('/<int:id>', methods=['PUT'])
@mechanic_token_required  # Only mechanics can update inventory
def update_inventory(current_mechanic_id, id):
    """PUT '/<int:id>': Updates a specific Inventory item (mechanic only)"""
    # Mechanics need to update stock levels and prices
    inventory = Inventory.query.get_or_404(id)
    try:
        updated_inventory = inventory_schema.load(request.json, instance=inventory, partial=True)
        db.session.commit()
        # Cache will expire automatically after 5 minutes
        return inventory_schema.jsonify(updated_inventory), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@inventory_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_token_required  # Only mechanics can delete inventory
@limiter.limit("5 per minute")  # Rate limit for delete operations - safety measure
def delete_inventory(current_mechanic_id, id):
    """DELETE '/<int:id>': Deletes a specific Inventory item (mechanic only)"""
    # Careful with deletions - might want to soft delete in production
    inventory = Inventory.query.get_or_404(id)
    try:
        db.session.delete(inventory)
        db.session.commit()
        # Cache will expire automatically after 5 minutes
        return jsonify({'message': 'Inventory item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
