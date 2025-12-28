"""Main routes - Homepage and general pages"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import ComicSeries, ImageAlbum, Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """Homepage"""
    tag_filter = request.args.get('tag')
    show_favorites = request.args.get('favorites') == 'true'
    sort_by = request.args.get('sort', 'date')  # Default sort by date
    
    series_query = ComicSeries.query
    albums_query = ImageAlbum.query.filter(ImageAlbum.series_id == None)
    
    if show_favorites:
        series_query = series_query.filter_by(is_favorite=True)
        albums_query = albums_query.filter_by(is_favorite=True)
        
    if tag_filter:
        series_query = series_query.join(ComicSeries.tags).filter(Tag.name == tag_filter)
        albums_query = albums_query.join(ImageAlbum.tags).filter(Tag.name == tag_filter)

    # Apply sorting
    if sort_by == 'date':
        series_query = series_query.order_by(ComicSeries.created_at.desc())
        albums_query = albums_query.order_by(ImageAlbum.created_at.desc())
    else:  # default: name
        series_query = series_query.order_by(ComicSeries.name)
        albums_query = albums_query.order_by(ImageAlbum.name)

    series_list = series_query.all()
    standalone_albums = albums_query.all()
    all_tags = Tag.query.all()
    
    return render_template('index.html', 
                           albums=standalone_albums, 
                           series_list=series_list,
                           tags=all_tags,
                           current_tag=tag_filter,
                           show_favorites=show_favorites,
                           current_sort=sort_by)
