"""
Mechanic routes for the API
This handles all mechanic-related endpoints
"""
from flask import request, jsonify
from sqlalchemy import func
from app.blueprints.mechanic import mechanic_bp
from app.models import Mechanic, ServiceTicket
from app.blueprints.mechanic.schema import mechanic_schema, mechanics_schema, mechanic_login_schema, MechanicSchema
from app.extention import db, limiter
from app.auth import encode_mechanic_token, mechanic_token_required


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    """POST '/' : Creates a new Mechanic"""
    # Schema now handles password hashing automatically
    try:
        mechanic_data = mechanic_schema.load(request.json)
        db.session.add(mechanic_data)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic_data), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating mechanic: {e}") 
        return jsonify({'error': str(e)}), 400


@mechanic_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit login attempts - assignment requirement
def mechanic_login():
    """POST '/login': Mechanic login (separate from customer login)"""
    # This was the optional challenge part 
    try:
        login_data = mechanic_login_schema.load(request.json)
        mechanic = Mechanic.query.filter_by(email=login_data['email']).first()
        
        if mechanic and mechanic.check_password(login_data['password']):
            token = encode_mechanic_token(mechanic.id)  # different token type for mechanics
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'mechanic': mechanic_schema.dump(mechanic)
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    """GET '/': Retrieves all Mechanics"""
    # Simple endpoint, no auth needed for viewing mechanics
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.route('/by-tickets', methods=['GET'])
def get_mechanics_by_tickets():
    """
    GET '/by-tickets': Get mechanics ordered by most tickets worked on
    This is the advanced query requirement from the assignment
    """
    mechanics = (db.session.query(Mechanic)
                .join(Mechanic.service_tickets)
                .group_by(Mechanic.id)
                .order_by(func.count(ServiceTicket.id).desc())
                .all())
    
    # Add ticket count to each mechanic's data
    result = []
    for mechanic in mechanics:
        mechanic_data = mechanic_schema.dump(mechanic)
        mechanic_data['ticket_count'] = len(mechanic.service_tickets)
        result.append(mechanic_data)
    
    return jsonify(result), 200


@mechanic_bp.route('/<int:id>', methods=['PUT'])
@mechanic_token_required  # Only authenticated mechanics can update
def update_mechanic(current_mechanic_id, id):
    """PUT '/<int:id>': Updates a specific Mechanic (employee access)"""
    # Employees can update any mechanic record for business operations
    
    try:
        mechanic = Mechanic.query.get_or_404(id)
        
        # Set the instance on the schema for updates
        update_schema = MechanicSchema()
        update_schema.instance = mechanic
        
        # Load the updated data
        updated_mechanic = update_schema.load(request.json, partial=True)
        
        db.session.commit()
        return mechanic_schema.jsonify(updated_mechanic), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@mechanic_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_token_required  # Authentication required for deletes
def delete_mechanic(current_mechanic_id, id):
    """DELETE '/<int:id>': Deletes a specific Mechanic (employee access)"""
    # Employees can delete any mechanic record for business operations
    
    try:
        mechanic = Mechanic.query.get_or_404(id)
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({'message': 'Mechanic deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400