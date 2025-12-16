"""Development configuration"""
from config.base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BaseConfig.DATA_DIR}/instance/database.db'
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging
