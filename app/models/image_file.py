"""Image File Model"""
from app import db

class ImageFile(db.Model):
    """Represents an individual image file"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    album_id = db.Column(db.Integer, db.ForeignKey('image_album.id'))
    album = db.relationship('ImageAlbum', backref=db.backref('images', lazy=True, cascade="all, delete-orphan"))
    
    def __repr__(self):
        return f'<ImageFile {self.filename}>'
