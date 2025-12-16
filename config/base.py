"""Base configuration"""
import os
from pathlib import Path

class BaseConfig:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB
    
    # Folders
    UPLOAD_FOLDER = str(DATA_DIR / 'uploads')
    ALBUM_FOLDER = str(DATA_DIR / 'albums')
    COVER_FOLDER = str(DATA_DIR / 'covers')
    INSTANCE_FOLDER = str(DATA_DIR / 'instance')
    
    # Encryption
    KEY_FILE = str(BASE_DIR / 'secret.key')
