from flask import Flask
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from app.extention import db, ma, migrate, limiter, cache

def create_app(config_name='development'):
    """
    Application factory function that creates and configures Flask app instances
    
    Args:
        config_name (str): Configuration environment ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Configure the application based on environment
    config_mapping = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    app.config.from_object(config_mapping.get(config_name, DevelopmentConfig))
    
    # Initialize extensions with the app
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def initialize_extensions(app):
    """Initialize Flask extensions with app instance"""
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app import models

def register_blueprints(app):
    """Register all blueprints with the application"""
    # Import blueprints
    from app.blueprints.customer import customer_bp
    from app.blueprints.mechanic import mechanic_bp
    from app.blueprints.service_ticket import service_ticket_bp
    from app.blueprints.inventory import inventory_bp
    
    # Register blueprints with URL prefixes
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

def register_error_handlers(app):
    """Register error handlers for the application"""
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500