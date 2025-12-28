"""Album routes - Album and chapter management"""
import os
import shutil
import mimetypes
from flask import Blueprint, request, redirect, url_for, render_template, send_file, current_app, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import ComicSeries, ImageAlbum, ImageFile, Tag
from app.services import EncryptionService
from app.utils import natural_sort_key

album_bp = Blueprint('album', __name__, url_prefix='/album')

@album_bp.route('/<int:id>')
@login_required
def view_album(id):
    """View album in reader"""
    album = ImageAlbum.query.get_or_404(id)
    images = ImageFile.query.filter_by(album_id=id).order_by(ImageFile.filename).all()
    
    prev_id = None
    next_id = None
    
    if album.series_id:
        series = ComicSeries.query.get(album.series_id)
        if series:
            siblings = sorted(series.albums, key=lambda x: natural_sort_key(x.name))
            current_index = next((i for i, item in enumerate(siblings) if item.id == album.id), -1)
            
            if current_index != -1:
                if current_index > 0:
                    prev_id = siblings[current_index - 1].id
                if current_index < len(siblings) - 1:
                    next_id = siblings[current_index + 1].id
    
    return render_template('viewer.html',
                         album_name=album.name,
                         album_id=album.id,
                         images=images,
                         prev_id=prev_id,
                         next_id=next_id)

@album_bp.route('/details/<type>/<int:id>')
@login_required
def details(type, id):
    """Show album or series details"""
    has_cover = False
    cover_filename = ''
    item = None
    extra_context = {}
    
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
        if item.cover_image:
            has_cover = True
            cover_filename = item.cover_image
        
        first_img = ImageFile.query.filter_by(album_id=id).order_by(ImageFile.filename).first()
        all_series = ComicSeries.query.all()
        
        extra_context = {
            'image_count': len(item.images),
            'first_image_url': url_for('album.get_image', album_id=item.id, filename=first_img.filename) if first_img else '',
            'view_url': url_for('album.view_album', id=item.id),
            'all_series': all_series,
            'current_series_id': item.series_id
        }
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
        if item.cover_image:
            has_cover = True
            cover_filename = item.cover_image
        
        chapters = sorted(item.albums, key=lambda x: natural_sort_key(x.name))
        extra_context = {
            'chapters': chapters,
            'is_completed': item.is_completed
        }
    
    return render_template('details.html',
                         type=type,
                         id=id,
                         item=item,
                         item_name=item.name,
                         has_cover=has_cover,
                         cover_filename=cover_filename,
                         rename_url=url_for('album.rename', type=type, id=id),
                         change_cover_url=url_for('album.change_cover', type=type, id=id),
                         delete_url=url_for('album.delete', type=type, id=id),
                         toggle_favorite_url=url_for('album.toggle_favorite', type=type, id=id),
                         add_tag_url=url_for('album.add_tag', type=type, id=id),
                         remove_tag_url=url_for('album.remove_tag', type=type, id=id),
                         all_tags=Tag.query.all(),
                         **extra_context)

@album_bp.route('/image/<int:album_id>/<filename>')
@login_required
def get_image(album_id, filename):
    """Serve decrypted image"""
    album = ImageAlbum.query.get_or_404(album_id)
    file_path = os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path, filename)
    
    if not os.path.exists(file_path):
        current_app.logger.error(f"File not found: {file_path}")
        current_app.logger.error(f"Album folder: {album.folder_path}")
        current_app.logger.error(f"Album folder full path: {os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path)}")
        if os.path.exists(os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path)):
            current_app.logger.error(f"Files in album folder: {os.listdir(os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path))}")
        return f"File not found: {filename}", 404
    
    try:
        encryption_service = EncryptionService(current_app.config['KEY_FILE'])
        decrypted_file = encryption_service.get_decrypted_file(file_path)
        
        mimetype, _ = mimetypes.guess_type(filename)
        if mimetype is None:
            mimetype = 'application/octet-stream'
        
        return send_file(decrypted_file, mimetype=mimetype)
    except Exception as e:
        current_app.logger.error(f"Error serving image {filename}: {e}")
        return f"Error serving image: {str(e)}", 500

@album_bp.route('/cover/<filename>')
@login_required
def get_cover(filename):
    """Serve cover image"""
    from flask import send_from_directory
    return send_from_directory(current_app.config['COVER_FOLDER'], filename)

@album_bp.route('/rename/<type>/<int:id>', methods=['POST'])
@login_required
def rename(type, id):
    """Rename album or series"""
    new_name = request.form.get('new_name')
    if not new_name:
        return redirect(request.referrer)
    
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
    else:
        return redirect(request.referrer)
    
    item.name = new_name
    db.session.commit()
    return redirect(request.referrer)

@album_bp.route('/change_cover/<type>/<int:id>', methods=['POST'])
@login_required
def change_cover(type, id):
    """Change cover image"""
    import time
    from PIL import Image
    import io
    
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
    else:
        return redirect(request.referrer)
    
    file = request.files.get('cover_file')
    
    if file and file.filename != '':
        ext = os.path.splitext(file.filename)[1]
        new_filename = f"cover_{type}_{id}_{int(time.time())}{ext}"
        save_path = os.path.join(current_app.config['COVER_FOLDER'], new_filename)
        file.save(save_path)
        
        # Delete old cover
        if item.cover_image:
            old_path = os.path.join(current_app.config['COVER_FOLDER'], item.cover_image)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        item.cover_image = new_filename
    else:
        # Delete cover
        if request.form.get('action') == 'delete_cover' and item.cover_image:
            old_path = os.path.join(current_app.config['COVER_FOLDER'], item.cover_image)
            if os.path.exists(old_path):
                os.remove(old_path)
            item.cover_image = None
    
    db.session.commit()
    return redirect(request.referrer)

@album_bp.route('/set_cover_from_page/<int:album_id>/<filename>', methods=['POST'])
@login_required
def set_cover_from_page(album_id, filename):
    """Set cover image from album page"""
    import time
    from PIL import Image
    import io
    
    album = ImageAlbum.query.get_or_404(album_id)
    file_path = os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Decrypt and load image
        encryption_service = EncryptionService(current_app.config['KEY_FILE'])
        decrypted_file = encryption_service.get_decrypted_file(file_path)
        decrypted_data = decrypted_file.getvalue()
        
        # Debug: Check if data looks like an image
        if len(decrypted_data) < 10:
            return jsonify({'error': 'Decrypted data too small'}), 500
        
        # Check file signature (first few bytes)
        file_signature = decrypted_data[:10].hex()
        print(f"File: {filename}, Size: {len(decrypted_data)}, Signature: {file_signature}")
        
        # Convert to JPG for smaller file size
        try:
            img = Image.open(io.BytesIO(decrypted_data))
        except Exception as pil_error:
            print(f"PIL error opening image: {pil_error}")
            # Try to identify the format from the data
            import imghdr
            img_format = imghdr.what(None, h=decrypted_data[:32])
            print(f"Detected format: {img_format}")
            if img_format:
                # Try opening with format hint
                img = Image.open(io.BytesIO(decrypted_data))
                img.verify()  # Verify the image is not corrupted
                img = Image.open(io.BytesIO(decrypted_data))  # Re-open after verify
            else:
                raise Exception(f"Cannot identify image format. PIL error: {pil_error}")
        
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Save as cover
        os.makedirs(current_app.config['COVER_FOLDER'], exist_ok=True)
        new_filename = f"cover_album_{album_id}_{int(time.time())}.jpg"
        save_path = os.path.join(current_app.config['COVER_FOLDER'], new_filename)
        img.save(save_path, 'JPEG', quality=90)
        
        # Delete old cover
        if album.cover_image:
            old_path = os.path.join(current_app.config['COVER_FOLDER'], album.cover_image)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        album.cover_image = new_filename
        db.session.commit()
        
        return jsonify({'success': True, 'cover': new_filename})
        
    except Exception as e:
        print(f"Error setting cover from page: {e}")
        print(f"File: {filename}, Path: {file_path}")
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

@album_bp.route('/delete/<type>/<int:id>', methods=['POST'])
@login_required
def delete(type, id):
    """Delete album or series"""
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
        folder_path = os.path.join(current_app.config['ALBUM_FOLDER'], item.folder_path)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        db.session.delete(item)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
        for album in item.albums:
            album.series_id = None
        db.session.delete(item)
    
    db.session.commit()
    return redirect(url_for('main.index'))

@album_bp.route('/add_to_series/<int:album_id>', methods=['POST'])
@login_required
def add_to_series(album_id):
    """Add album to series"""
    import shutil
    
    album = ImageAlbum.query.get_or_404(album_id)
    series_id = request.form.get('series_id')
    
    if series_id and series_id != "0":
        album.series_id = int(series_id)
        series = ComicSeries.query.get(int(series_id))
        
        # Auto-set series cover from chapter 1
        if series:
            chapters = sorted(series.albums, key=lambda x: natural_sort_key(x.name))
            if chapters and chapters[0].id == album_id:
                # This is chapter 1, copy its cover to series
                if album.cover_image:
                    # Copy album cover to series
                    album_cover_path = os.path.join(current_app.config['COVER_FOLDER'], album.cover_image)
                    if os.path.exists(album_cover_path):
                        import time
                        ext = os.path.splitext(album.cover_image)[1]
                        new_series_cover = f"cover_series_{series.id}_{int(time.time())}{ext}"
                        series_cover_path = os.path.join(current_app.config['COVER_FOLDER'], new_series_cover)
                        shutil.copy2(album_cover_path, series_cover_path)
                        
                        # Delete old series cover
                        if series.cover_image:
                            old_path = os.path.join(current_app.config['COVER_FOLDER'], series.cover_image)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                        
                        series.cover_image = new_series_cover
                else:
                    # Use first image from album as cover
                    first_img = ImageFile.query.filter_by(album_id=album_id).order_by(ImageFile.filename).first()
                    if first_img:
                        from PIL import Image
                        import io
                        import time
                        
                        file_path = os.path.join(current_app.config['ALBUM_FOLDER'], album.folder_path, first_img.filename)
                        if os.path.exists(file_path):
                            try:
                                encryption_service = EncryptionService(current_app.config['KEY_FILE'])
                                decrypted_file = encryption_service.get_decrypted_file(file_path)
                                decrypted_data = decrypted_file.getvalue()
                                
                                new_series_cover = f"cover_series_{series.id}_{int(time.time())}.jpg"
                                save_path = os.path.join(current_app.config['COVER_FOLDER'], new_series_cover)
                                
                                try:
                                    img = Image.open(io.BytesIO(decrypted_data))
                                except Exception as pil_error:
                                    print(f"PIL error opening image for series cover: {pil_error}")
                                    import imghdr
                                    img_format = imghdr.what(None, h=decrypted_data[:32])
                                    print(f"Detected format: {img_format}")
                                    if img_format:
                                        img = Image.open(io.BytesIO(decrypted_data))
                                        img.verify()
                                        img = Image.open(io.BytesIO(decrypted_data))
                                    else:
                                        raise Exception(f"Cannot identify image format. PIL error: {pil_error}")
                                
                                if img.mode in ('RGBA', 'LA', 'P'):
                                    img = img.convert('RGB')
                                img.save(save_path, 'JPEG', quality=90)
                                
                                # Delete old series cover
                                if series.cover_image:
                                    old_path = os.path.join(current_app.config['COVER_FOLDER'], series.cover_image)
                                    if os.path.exists(old_path):
                                        os.remove(old_path)
                                
                                series.cover_image = new_series_cover
                            except Exception as e:
                                print(f"Error creating series cover from first image: {e}")
                                print(f"File: {first_img.filename}, Path: {file_path}")
                                # Continue without setting cover
    else:
        album.series_id = None
    
    db.session.commit()
    return redirect(request.referrer)

@album_bp.route('/remove_from_series/<int:album_id>', methods=['POST'])
@login_required
def remove_from_series(album_id):
    """Remove album from series"""
    album = ImageAlbum.query.get_or_404(album_id)
    album.series_id = None
    db.session.commit()
    return redirect(request.referrer)

@album_bp.route('/toggle_favorite/<type>/<int:id>', methods=['POST'])
@login_required
def toggle_favorite(type, id):
    """Toggle favorite status"""
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
    else:
        return redirect(request.referrer)
    
    item.is_favorite = not item.is_favorite
    db.session.commit()
    return redirect(request.referrer)

@album_bp.route('/add_tag/<type>/<int:id>', methods=['POST'])
@login_required
def add_tag(type, id):
    """Add tag to item"""
    tag_name = request.form.get('tag_name')
    if not tag_name:
        return redirect(request.referrer)
    
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
    else:
        return redirect(request.referrer)
    
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
    
    if tag not in item.tags:
        item.tags.append(tag)
        db.session.commit()
        
    return redirect(request.referrer)

@album_bp.route('/remove_tag/<type>/<int:id>', methods=['POST'])
@login_required
def remove_tag(type, id):
    """Remove tag from item"""
    tag_id = request.form.get('tag_id')
    
    if type == 'album':
        item = ImageAlbum.query.get_or_404(id)
    elif type == 'series':
        item = ComicSeries.query.get_or_404(id)
    else:
        return redirect(request.referrer)
        
    tag = Tag.query.get(tag_id)
    if tag and tag in item.tags:
        item.tags.remove(tag)
        db.session.commit()
        
    return redirect(request.referrer)
