"""Image Service"""
import os
import time
from werkzeug.utils import secure_filename
from app.utils.sorting import natural_sort_key

class ImageService:
    """Handles image-related operations"""
    
    def __init__(self, app_config, encryption_service):
        self.config = app_config
        self.encryption_service = encryption_service
    
    def process_folder_upload(self, files, db_session):
        """Process folder upload"""
        from app.models import ImageAlbum, ImageFile
        
        if not files or files[0].filename == '':
            raise ValueError("No files provided")
        
        # Sort files
        files.sort(key=lambda x: natural_sort_key(x.filename))
        
        # Get folder name
        first_path = files[0].filename
        folder_name = first_path.split('/')[0] if '/' in first_path else "Album"
        safe_folder_name = secure_filename(folder_name) + "_" + str(int(time.time()))
        abs_folder_path = os.path.join(self.config['ALBUM_FOLDER'], safe_folder_name)
        os.makedirs(abs_folder_path)
        
        # Create album
        new_album = ImageAlbum(name=folder_name, folder_path=safe_folder_name)
        db_session.add(new_album)
        db_session.commit()
        
        # Process files
        for file in files:
            if file.filename and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                safe_img_name = secure_filename(os.path.basename(file.filename))
                count = len(new_album.images) + 1
                final_filename = f"{count:04d}_{safe_img_name}"
                save_path = os.path.join(abs_folder_path, final_filename)
                
                # Encrypt and save
                img_data = file.read()
                self.encryption_service.save_encrypted(img_data, save_path)
                
                img_record = ImageFile(filename=final_filename, album_id=new_album.id)
                db_session.add(img_record)
        
        db_session.commit()
        return new_album
