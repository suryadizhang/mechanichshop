"""
Configuration settings for the Mechanic Shop API
"""
import os


class Config:
    """Base configuration class with common settings"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "13Agustus"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 'sqlite:///mechanic_shop.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Saves memory

    # API Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # Flask-Limiter Configuration (assignment requirement)
    RATELIMIT_STORAGE_URL = (
        "redis://localhost:6379" if os.environ.get('REDIS_URL')
        else "memory://"  # Falls back to memory if no Redis
    )
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"  # Default rate limits

    # Flask-Caching Configuration (assignment requirement)
    CACHE_TYPE = "SimpleCache"  # Simple in-memory cache for development
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL') or
        'sqlite:///mechanic_shop.db'  # Use SQLite for development
    )


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    # In-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
