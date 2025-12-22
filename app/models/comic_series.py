"""Comic Series Model"""
from app import db
from app.models.tag import series_tags

class ComicSeries(db.Model):
    """Represents a comic series/collection"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    cover_image = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=series_tags, lazy='subquery',
        backref=db.backref('series', lazy=True))
    albums = db.relationship('ImageAlbum', backref='series', lazy=True)
    
    def __repr__(self):
        return f'<ComicSeries {self.name}>'
