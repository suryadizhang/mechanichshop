"""
Customer routes for the API
This handles all the customer-related endpoints
"""
from flask import request, jsonify
from app.blueprints.customer import customer_bp
from app.models import Customer, ServiceTicket
from app.blueprints.customer.schema import (
    customer_schema, customers_schema, login_schema, CustomerSchema
)
from app.blueprints.service_ticket.schema import service_tickets_schema
from app.extention import db, limiter, cache
from app.auth import encode_token, token_required


@customer_bp.route('/', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes - assignment requirement
def get_customers():
    """Get all customers with pagination (assignment requirement)"""
    # Get page parameters from request
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)

    # Paginate the query
    customers = Customer.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Return paginated results with metadata
    result = {
        'customers': customers_schema.dump(customers.items),
        'pagination': {
            'page': customers.page,
            'pages': customers.pages,
            'per_page': customers.per_page,
            'total': customers.total,
            'has_prev': customers.has_prev,
            'has_next': customers.has_next
        }
    }
    return jsonify(result), 200


@customer_bp.route('/', methods=['POST'])
def create_customer():
    """Create a new customer"""
    try:
        # Schema now handles password hashing automatically
        customer_data = customer_schema.load(request.json)
        db.session.add(customer_data)
        db.session.commit()
        # Clear cache after creating new customer
        cache.delete_memoized(get_customers)
        return customer_schema.jsonify(customer_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit login attempts
def login():
    """POST '/login': Customer login"""
    try:
        login_data = login_schema.load(request.json)
        customer = Customer.query.filter_by(email=login_data['email']).first()

        if customer and customer.check_password(login_data['password']):
            token = encode_token(customer.id)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'customer': customer_schema.dump(customer)
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(current_customer_id):
    """GET '/my-tickets': Get service tickets for authenticated customer"""
    try:
        tickets = ServiceTicket.query.filter_by(
            customer_id=current_customer_id
        ).all()
        return service_tickets_schema.jsonify(tickets), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    """Get a specific customer"""
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer), 200


@customer_bp.route('/', methods=['PUT'])
@token_required
def update_current_customer(current_customer_id):
    """PUT '/': Updates the current authenticated customer's profile"""
    # Customers can update their own profile

    customer = Customer.query.get_or_404(current_customer_id)

    try:
        # Set the instance on the schema for updates
        update_schema = CustomerSchema()
        update_schema.instance = customer

        # Load the updated data
        updated_customer = update_schema.load(request.json, partial=True)

        db.session.commit()
        # Clear cache after update
        cache.delete_memoized(get_customers)
        return customer_schema.jsonify(updated_customer), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(current_customer_id, id):
    """PUT '/<int:id>': Updates a specific customer by ID"""
    # Only allow customers to update their own profile
    if current_customer_id != id:
        return jsonify({'error': 'You can only update your own profile'}), 403

    try:
        customer = Customer.query.get_or_404(id)

        # Set the instance on the schema for updates
        update_schema = CustomerSchema()
        update_schema.instance = customer

        # Load the updated data
        updated_customer = update_schema.load(request.json, partial=True)

        db.session.commit()
        # Clear cache after update
        cache.delete_memoized(get_customers)
        return customer_schema.jsonify(updated_customer), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/', methods=['DELETE'])
@token_required
def delete_current_customer(current_customer_id):
    """DELETE '/': Deletes the current authenticated customer's account"""
    # Customers can delete their own account

    customer = Customer.query.get_or_404(current_customer_id)
    try:
        db.session.delete(customer)
        db.session.commit()
        # Clear cache after deletion
        cache.delete_memoized(get_customers)
        return jsonify({
            'message': 'Customer account deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(current_customer_id, id):
    """DELETE '/<int:id>': Deletes a specific customer by ID"""
    # Only allow customers to delete their own account
    if current_customer_id != id:
        return jsonify({'error': 'You can only delete your own account'}), 403

    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        # Clear cache after deletion
        cache.delete_memoized(get_customers)
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
