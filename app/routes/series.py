"""Series routes - Comic series management"""
from flask import Blueprint, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import ComicSeries

series_bp = Blueprint('series', __name__, url_prefix='/series')

@series_bp.route('/create', methods=['POST'])
@login_required
def create_series():
    """Create new series"""
    name = request.form.get('series_name')
    if name:
        new_series = ComicSeries(name=name)
        db.session.add(new_series)
        db.session.commit()
    return redirect(url_for('main.index'))

@series_bp.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_status(id):
    """Toggle series completion status"""
    series = ComicSeries.query.get_or_404(id)
    series.is_completed = not series.is_completed
    db.session.commit()
    return redirect(request.referrer or url_for('main.index'))
