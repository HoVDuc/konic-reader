"""Comic Series Model"""
from app import db

class ComicSeries(db.Model):
    """Represents a comic series/collection"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    cover_image = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean, default=False)
    albums = db.relationship('ImageAlbum', backref='series', lazy=True)
    
    def __repr__(self):
        return f'<ComicSeries {self.name}>'
