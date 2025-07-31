from flask import request, jsonify
from app.blueprints.mechanic import mechanic_bp
from app.models import Mechanic
from app.blueprints.mechanic.schema import mechanic_schema, mechanics_schema
from app.extention import db

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    """POST '/' : Creates a new Mechanic"""
    try:
        mechanic_data = mechanic_schema.load(request.json)
        db.session.add(mechanic_data)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    """GET '/': Retrieves all Mechanics"""
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    """PUT '/<int:id>': Updates a specific Mechanic based on the id"""
    try:
        mechanic = Mechanic.query.get_or_404(id)
        updated_mechanic = mechanic_schema.load(request.json, instance=mechanic, partial=True)
        db.session.commit()
        return mechanic_schema.jsonify(updated_mechanic), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    """DELETE '/<int:id>': Deletes a specific Mechanic based on the id"""
    try:
        mechanic = Mechanic.query.get_or_404(id)
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({'message': 'Mechanic deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400