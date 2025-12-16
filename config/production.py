"""Production configuration"""
import os
from config.base import BaseConfig

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with environment variable if available
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{BaseConfig.DATA_DIR}/instance/database.db'
    )
    SQLALCHEMY_ECHO = False
