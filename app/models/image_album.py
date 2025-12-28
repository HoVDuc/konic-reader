"""Image Album Model"""
from app import db
from app.models.tag import album_tags
from datetime import datetime

class ImageAlbum(db.Model):
    """Represents an album/chapter"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    folder_path = db.Column(db.String(300))
    cover_image = db.Column(db.String(300))
    series_id = db.Column(db.Integer, db.ForeignKey('comic_series.id'), nullable=True)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=album_tags, lazy='subquery',
        backref=db.backref('albums', lazy=True))
    
    def __repr__(self):
        return f'<ImageAlbum {self.name}>'
