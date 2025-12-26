"""Flask application factory"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import models (needed before db.create_all)
    from app.models import ComicSeries, ImageAlbum, ImageFile, User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.upload import upload_bp
    from app.routes.series import series_bp
    from app.routes.album import album_bp
    from app.routes.api import api_bp
    from app.routes.tags import tags_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(series_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(auth_bp)
    
    return app
