"""Image Album Model"""
from app import db

class ImageAlbum(db.Model):
    """Represents an album/chapter"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    folder_path = db.Column(db.String(300))
    cover_image = db.Column(db.String(300))
    series_id = db.Column(db.Integer, db.ForeignKey('comic_series.id'), nullable=True)
    
    def __repr__(self):
        return f'<ImageAlbum {self.name}>'
