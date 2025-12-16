"""Routes package"""
from app.routes.main import main_bp
from app.routes.upload import upload_bp
from app.routes.series import series_bp
from app.routes.album import album_bp
from app.routes.api import api_bp

__all__ = ['main_bp', 'upload_bp', 'series_bp', 'album_bp', 'api_bp']
