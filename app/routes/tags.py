from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Tag

tags_bp = Blueprint('tags', __name__, url_prefix='/tags')

@tags_bp.route('/')
def manage_tags():
    """List all tags for management and filtering"""
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags.html', tags=all_tags)

@tags_bp.route('/edit/<int:id>', methods=['POST'])
def edit_tag(id):
    """Edit tag name"""
    tag = Tag.query.get_or_404(id)
    new_name = request.form.get('name')
    
    if new_name and new_name != tag.name:
        # Check if name exists
        existing = Tag.query.filter_by(name=new_name).first()
        if existing:
            # Merge? Or Error? For now, error or simple skip
            pass 
        else:
            tag.name = new_name
            db.session.commit()
            
    return redirect(url_for('tags.manage_tags'))

@tags_bp.route('/delete/<int:id>', methods=['POST'])
def delete_tag(id):
    """Delete tag"""
    tag = Tag.query.get_or_404(id)
    
    # Remove associations (SQLAlchemy usually handles this if configured, but let's be safe)
    # The secondary tables should handle deletion if cascade is set, but we didn't set cascade explicitly in models.
    # However, removing the Tag object will remove rows from association tables in many configurations.
    # Let's try standard delete.
    
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags.manage_tags'))
