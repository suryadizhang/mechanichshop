from flask import request, jsonify
from app.blueprints.service_ticket import service_ticket_bp
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_ticket.schema import service_ticket_schema, service_tickets_schema
from app.extention import db

@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    """POST '/': Pass in all the required information to create the service_ticket"""
    try:
        ticket_data = service_ticket_schema.load(request.json)
        db.session.add(ticket_data)
        db.session.commit()
        return service_ticket_schema.jsonify(ticket_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    """PUT '/<ticket_id>/assign-mechanic/<mechanic_id>': Adds relationship between service ticket and mechanic"""
    try:
        ticket = ServiceTicket.query.get_or_404(ticket_id)
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        
        # Check if mechanic is already assigned
        if mechanic not in ticket.mechanics:
            # Use relationship attributes to treat the relationship like a list
            ticket.mechanics.append(mechanic)
            ticket.status = 'In Progress'  # Update status when mechanic is assigned
            db.session.commit()
            return jsonify({'message': f'Mechanic {mechanic_id} assigned to ticket {ticket_id}'}), 200
        else:
            return jsonify({'message': 'Mechanic already assigned to this ticket'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    """PUT '/<ticket_id>/remove-mechanic/<mechanic_id>': Removes relationship from service ticket and mechanic"""
    try:
        ticket = ServiceTicket.query.get_or_404(ticket_id)
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        
        # Check if mechanic is assigned to this ticket
        if mechanic in ticket.mechanics:
            # Use relationship attributes to treat the relationship like a list
            ticket.mechanics.remove(mechanic)
            # Reset status if no mechanics are assigned
            if not ticket.mechanics:
                ticket.status = 'Open'
            db.session.commit()
            return jsonify({'message': f'Mechanic {mechanic_id} removed from ticket {ticket_id}'}), 200
        else:
            return jsonify({'error': 'Mechanic not assigned to this ticket'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    """GET '/': Retrieves all service tickets"""
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200