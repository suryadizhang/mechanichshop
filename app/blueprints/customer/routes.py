from flask import request, jsonify
from app.blueprints.customer import customer_bp
from app.models import Customer
from app.blueprints.customer.schema import customer_schema, customers_schema
from app.extention import db

@customer_bp.route('/', methods=['GET'])
def get_customers():
    """Get all customers"""
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200

@customer_bp.route('/', methods=['POST'])
def create_customer():
    """Create a new customer"""
    try:
        customer_data = customer_schema.load(request.json)
        db.session.add(customer_data)
        db.session.commit()
        return customer_schema.jsonify(customer_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    """Get a specific customer"""
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer), 200

@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    """Update a customer"""
    try:
        customer = Customer.query.get_or_404(id)
        updated_customer = customer_schema.load(request.json, instance=customer, partial=True)
        db.session.commit()
        return customer_schema.jsonify(updated_customer), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """Delete a customer"""
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400