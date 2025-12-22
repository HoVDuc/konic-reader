from app import db

album_tags = db.Table('album_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('image_album.id'), primary_key=True)
)

series_tags = db.Table('series_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('series_id', db.Integer, db.ForeignKey('comic_series.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'
