"""ZIP Processing Service"""
import os
import time
import zipfile
import io
from PIL import Image
from werkzeug.utils import secure_filename
from app.utils.sorting import natural_sort_key

class ZIPProcessor:
    """Handles ZIP extraction and processing"""
    
    def __init__(self, app_config, encryption_service):
        self.config = app_config
        self.encryption_service = encryption_service
    
    def process_zip(self, zip_path, original_filename, db_session, progress_callback=None):
        """Process ZIP file and extract encrypted images"""
        from app.models import ImageAlbum, ImageFile
        
        if progress_callback:
            progress_callback(5, 'Đang đọc file ZIP...')
        
        # Create album
        album_name = os.path.splitext(original_filename)[0]
        safe_folder_name = secure_filename(album_name) + "_" + str(int(time.time()))
        abs_folder_path = os.path.join(self.config['ALBUM_FOLDER'], safe_folder_name)
        os.makedirs(abs_folder_path)
        
        new_album = ImageAlbum(name=album_name, folder_path=safe_folder_name)
        db_session.add(new_album)
        db_session.commit()
        
        # Extract images
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            all_files = zip_ref.namelist()
            valid_images = [f for f in all_files 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')) 
                          and '__MACOSX' not in f]
            valid_images.sort(key=natural_sort_key)
            total_files = len(valid_images)
            
            if total_files == 0:
                raise Exception("File ZIP rỗng!")
            
            count = 0
            for file_in_zip in valid_images:
                count += 1
                percent = int((count / total_files) * 100)
                
                if progress_callback:
                    progress_callback(percent, f'Đang giải nén: {count}/{total_files}')
                
                try:
                    img_data = zip_ref.read(file_in_zip)
                    
                    # Convert to WebP
                    try:
                        img = Image.open(io.BytesIO(img_data))
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='WEBP', quality=90)
                        webp_data = img_byte_arr.getvalue()
                    except Exception as img_error:
                        print(f"Error converting image {file_in_zip} to WebP: {img_error}")
                        # Skip this image
                        continue
                    
                    safe_img_name = f"{count:04d}_extracted.webp"
                    save_path = os.path.join(abs_folder_path, safe_img_name)
                    
                    # Save encrypted
                    self.encryption_service.save_encrypted(webp_data, save_path)
                    
                    db_session.add(ImageFile(filename=safe_img_name, album_id=new_album.id))
                    
                    if count % 10 == 0:
                        db_session.commit()
                except Exception as e:
                    print(f"Error processing zip file {file_in_zip}: {e}")
                    continue
            
            db_session.commit()
        
        return new_album
