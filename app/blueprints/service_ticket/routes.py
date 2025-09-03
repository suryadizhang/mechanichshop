"""
Service ticket routes - the main workflow of the mechanic shop
This handles creating tickets, assigning mechanics, and adding parts

The many-to-many relationships were confusing but I think I got them working
The assignment wanted an edit route that can add/remove multiple mechanics
"""
from flask import request, jsonify
from app.blueprints.service_ticket import service_ticket_bp
from app.models import ServiceTicket, Mechanic, Inventory
from app.blueprints.service_ticket.schema import (
    service_ticket_schema, service_tickets_schema
)
from app.extention import db


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    """POST '/': Pass in all required information to create service_ticket"""
    # Anyone can create a service ticket for now
    try:
        ticket_data = service_ticket_schema.load(request.json)
        db.session.add(ticket_data)
        db.session.commit()
        return service_ticket_schema.jsonify(ticket_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route(
    '/<int:ticket_id>/assign-mechanic/<int:mechanic_id>',
    methods=['PUT']
)
def assign_mechanic(ticket_id, mechanic_id):
    """PUT '/<ticket_id>/assign-mechanic/<mechanic_id>': Adds relationship"""
    # This was easier than the bulk edit route below
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    try:
        # Check if mechanic is already assigned (avoid duplicates)
        if mechanic not in ticket.mechanics:
            # Use relationship attributes to treat the relationship like a list
            ticket.mechanics.append(mechanic)
            ticket.status = 'In Progress'  # Update status
            db.session.commit()
            return jsonify({
                'message': f'Mechanic {mechanic_id} assigned to {ticket_id}'
            }), 200
        else:
            return jsonify({
                'message': 'Mechanic already assigned to this ticket'
            }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route(
    '/<int:ticket_id>/remove-mechanic/<int:mechanic_id>',
    methods=['PUT']
)
def remove_mechanic(ticket_id, mechanic_id):
    """PUT '/<ticket_id>/remove-mechanic/<mechanic_id>': Remove mechanic"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    try:
        # Check if mechanic is assigned to this ticket
        if mechanic in ticket.mechanics:
            # Use relationship attributes to treat the relationship like a list
            ticket.mechanics.remove(mechanic)
            # Reset status if no mechanics are assigned
            if not ticket.mechanics:
                ticket.status = 'Open'
            db.session.commit()
            return jsonify({
                'message': f'Mechanic {mechanic_id} removed from {ticket_id}'
            }), 200
        else:
            return jsonify({
                'error': 'Mechanic not assigned to this ticket'
            }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    """
    PUT '/<int:ticket_id>/edit': Add and remove mechanics from a ticket
    This is the advanced query requirement - bulk operations
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    try:
        data = request.get_json()

        # Remove mechanics first
        remove_ids = data.get('remove_ids', [])
        for mechanic_id in remove_ids:
            mechanic = Mechanic.query.get(mechanic_id)
            if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

        # Then add new mechanics
        add_ids = data.get('add_ids', [])
        for mechanic_id in add_ids:
            mechanic = Mechanic.query.get(mechanic_id)
            if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

        # Update status based on whether we have mechanics assigned
        if ticket.mechanics:
            ticket.status = 'In Progress'
        else:
            ticket.status = 'Open'

        db.session.commit()
        return service_ticket_schema.jsonify(ticket), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route(
    '/<int:ticket_id>/add-part/<int:inventory_id>',
    methods=['PUT']
)
def add_part_to_ticket(ticket_id, inventory_id):
    """
    PUT '/<int:ticket_id>/add-part/<int:inventory_id>': Add part to ticket
    This connects inventory to service tickets - assignment requirement
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    inventory_item = Inventory.query.get_or_404(inventory_id)

    try:
        # Check if part is already added to this ticket (avoid duplicates)
        if inventory_item not in ticket.inventory_items:
            ticket.inventory_items.append(inventory_item)
            # Recalculate total cost when parts are added
            ticket.calculate_total_cost()  # method defined in the model
            db.session.commit()
            return jsonify({
                'message': f'Part {inventory_id} added to {ticket_id}'
            }), 200
        else:
            return jsonify({
                'message': 'Part already added to this ticket'
            }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    """GET '/': Retrieves all service tickets with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    tickets = ServiceTicket.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'service_tickets': service_tickets_schema.dump(tickets.items),
        'total': tickets.total,
        'pages': tickets.pages,
        'current_page': tickets.page,
        'has_next': tickets.has_next,
        'has_prev': tickets.has_prev
    }), 200


@service_ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
    """GET '/<int:ticket_id>': Retrieve a specific service ticket"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    return service_ticket_schema.jsonify(ticket), 200


@service_ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
    """PUT '/<int:ticket_id>': Updates a specific service ticket"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    try:
        updated_ticket = service_ticket_schema.load(
            request.json, instance=ticket, partial=True
        )
        db.session.commit()
        return service_ticket_schema.jsonify(updated_ticket), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@service_ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
    """DELETE '/<int:ticket_id>': Deletes a specific service ticket"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    try:
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'Service ticket deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
