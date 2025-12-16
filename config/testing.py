"""Testing configuration"""
from config.base import BaseConfig

class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
