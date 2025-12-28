"""Upload routes - Handle file uploads"""
import os
import uuid
import threading
from flask import Blueprint, request, jsonify, redirect, url_for, current_app, render_template
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.services import EncryptionService, PDFProcessor, ZIPProcessor, ImageService
from app.routes.api import update_progress

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/', methods=['GET'])
@login_required
def upload_page():
    """Render upload page"""
    return render_template('upload.html')

def get_services():
    """Get service instances"""
    encryption_service = EncryptionService(current_app.config['KEY_FILE'])
    pdf_processor = PDFProcessor(current_app.config, encryption_service)
    zip_processor = ZIPProcessor(current_app.config, encryption_service)
    image_service = ImageService(current_app.config, encryption_service)
    # torrent_service = TorrentService(current_app.config)
    return encryption_service, pdf_processor, zip_processor, image_service, None  # torrent_service

def process_pdf_background(task_id, temp_pdf_path, original_filename):
    """Background task for PDF processing"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            _, pdf_processor, _, _, _ = get_services()
            
            def progress_callback(percent, message):
                update_progress(task_id, 'processing', percent, message)
            
            pdf_processor.process_pdf(
                temp_pdf_path, 
                original_filename, 
                db.session, 
                progress_callback
            )
            
            os.remove(temp_pdf_path)
            update_progress(task_id, 'completed', 100, 'Hoàn tất!')
            
        except Exception as e:
            print(f"PDF Error: {e}")
            update_progress(task_id, 'error', 0, str(e))

def process_zip_background(task_id, temp_zip_path, original_filename):
    """Background task for ZIP processing"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            _, _, zip_processor, _, _ = get_services()
            
            def progress_callback(percent, message):
                update_progress(task_id, 'processing', percent, message)
            
            zip_processor.process_zip(
                temp_zip_path,
                original_filename,
                db.session,
                progress_callback
            )
            
            os.remove(temp_zip_path)
            update_progress(task_id, 'completed', 100, 'Hoàn tất!')
            
        except Exception as e:
            print(f"ZIP Error: {e}")
            update_progress(task_id, 'error', 0, str(e))

@upload_bp.route('/pdf', methods=['POST'])
@login_required
def upload_pdf():
    """Handle PDF upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No name'}), 400
    
    task_id = str(uuid.uuid4())
    safe_filename = secure_filename(file.filename)
    temp_pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(temp_pdf_path)
    
    thread = threading.Thread(
        target=process_pdf_background,
        args=(task_id, temp_pdf_path, safe_filename)
    )
    thread.start()
    
    return jsonify({'task_id': task_id})

@upload_bp.route('/zip', methods=['POST'])
@login_required
def upload_zip():
    """Handle ZIP upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No name'}), 400
    
    task_id = str(uuid.uuid4())
    safe_filename = secure_filename(file.filename)
    temp_zip_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(temp_zip_path)
    
    thread = threading.Thread(
        target=process_zip_background,
        args=(task_id, temp_zip_path, safe_filename)
    )
    thread.start()
    
    return jsonify({'task_id': task_id})

@upload_bp.route('/folder', methods=['POST'])
@login_required
def upload_folder():
    """Handle folder upload (supports multiple folders)"""
    if 'files' not in request.files:
        return "Lỗi: No files", 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return "Lỗi: Empty files", 400
    
    try:
        _, _, _, image_service, _ = get_services()
        # Check if multiple folders by looking at unique root folder names
        root_folders = set()
        for f in files:
            if f.filename and '/' in f.filename:
                root_folders.add(f.filename.split('/')[0])
        
        if len(root_folders) > 1:
            # Multiple folders
            image_service.process_multiple_folders(files, db.session)
        else:
            # Single folder
            image_service.process_folder_upload(files, db.session)
        
        return redirect(url_for('main.index'))
    except Exception as e:
        return f"Lỗi: {str(e)}", 500


def process_torrent_background(task_id, temp_torrent_path, original_filename):
    """Background task for torrent processing"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            encryption_service, _, _, image_service, torrent_service = get_services()
            
            def progress_callback(percent, message):
                update_progress(task_id, 'processing', percent, message)
            
            # Read the torrent file
            with open(temp_torrent_path, 'rb') as f:
                from werkzeug.datastructures import FileStorage
                import io
                
                # Create a FileStorage object
                torrent_file = FileStorage(
                    stream=io.BytesIO(f.read()),
                    filename=original_filename
                )
                
                torrent_service.import_from_torrent(
                    torrent_file,
                    db.session,
                    image_service,
                    progress_callback
                )
            
            os.remove(temp_torrent_path)
            update_progress(task_id, 'completed', 100, 'Hoàn tất!')
            
        except Exception as e:
            print(f"Torrent Error: {e}")
            import traceback
            traceback.print_exc()
            update_progress(task_id, 'error', 0, str(e))


@upload_bp.route('/torrent', methods=['POST'])
@login_required
def upload_torrent():
    """Handle torrent upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No name'}), 400
    
    task_id = str(uuid.uuid4())
    safe_filename = secure_filename(file.filename)
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    temp_torrent_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(temp_torrent_path)
    
    thread = threading.Thread(
        target=process_torrent_background,
        args=(task_id, temp_torrent_path, safe_filename)
    )
    thread.start()
    
    return jsonify({'task_id': task_id})
