"""Main routes - Homepage and general pages"""
from flask import Blueprint, render_template
from app.models import ComicSeries, ImageAlbum

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    series_list = ComicSeries.query.all()
    standalone_albums = ImageAlbum.query.filter(ImageAlbum.series_id == None).all()
    return render_template('index.html', albums=standalone_albums, series_list=series_list)
