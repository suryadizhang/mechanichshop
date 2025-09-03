"""
Authentication utilities for JWT tokens
This handles login tokens for both customers and mechanics
"""
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError


# Secret key for JWT tokens (should be in environment variables for production)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'your-secret-key-change-in-production'
)
ALGORITHM = 'HS256'  # Using HS256 algorithm for JWT


def encode_token(customer_id):
    """
    Create a JWT token for a customer login

    Args:
        customer_id (int): The customer's ID from the database

    Returns:
        str: JWT token that expires in 24 hours
    """
    payload = {
        'customer_id': customer_id,
        'user_type': 'customer',  # This helps distinguish customer vs mechanic tokens
        'exp': datetime.utcnow() + timedelta(hours=24),  # 24 hour expiry
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def encode_mechanic_token(mechanic_id):
    """
    Create a JWT token for a mechanic

    Args:
        mechanic_id (int): The mechanic's ID

    Returns:
        str: JWT token
    """
    payload = {
        'mechanic_id': mechanic_id,
        'user_type': 'mechanic',
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    """
    Decode a JWT token

    Args:
        token (str): JWT token

    Returns:
        dict: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def token_required(f):
    """
    Decorator that requires a valid customer token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401

        # Check if it's a customer token
        if payload.get('user_type') != 'customer':
            return jsonify({'error': 'Invalid token type'}), 401

        # Pass customer_id to the decorated function
        current_customer_id = payload.get('customer_id')
        return f(current_customer_id, *args, **kwargs)

    return decorated


def mechanic_token_required(f):
    """
    Decorator that requires a valid mechanic token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid token'}), 401

        # Check if it's a mechanic token
        if payload.get('user_type') != 'mechanic':
            return jsonify({'error': 'Invalid token type'}), 401

        # Pass mechanic_id to the decorated function
        current_mechanic_id = payload.get('mechanic_id')
        return f(current_mechanic_id, *args, **kwargs)

    return decorated
