"""PDF Processing Service"""
import os
import io
import time
from pdf2image import convert_from_path, pdfinfo_from_path
from werkzeug.utils import secure_filename

class PDFProcessor:
    """Handles PDF to image conversion"""
    
    def __init__(self, app_config, encryption_service):
        self.config = app_config
        self.encryption_service = encryption_service
    
    def process_pdf(self, pdf_path, original_filename, db_session, progress_callback=None):
        """Process PDF file and convert to encrypted images"""
        from app.models import ImageAlbum, ImageFile
        
        # Analyze PDF
        if progress_callback:
            progress_callback(5, 'Đang phân tích PDF...')
        
        info = pdfinfo_from_path(pdf_path)
        total_pages = info["Pages"]
        
        # Create album
        album_name = os.path.splitext(original_filename)[0]
        safe_folder_name = secure_filename(album_name) + "_" + str(int(time.time()))
        abs_folder_path = os.path.join(self.config['ALBUM_FOLDER'], safe_folder_name)
        os.makedirs(abs_folder_path)
        
        new_album = ImageAlbum(name=album_name, folder_path=safe_folder_name)
        db_session.add(new_album)
        db_session.commit()
        
        # Convert pages in chunks
        chunk_size = 5
        for i in range(1, total_pages + 1, chunk_size):
            last_page = min(i + chunk_size - 1, total_pages)
            percent = int((i / total_pages) * 100)
            
            if progress_callback:
                progress_callback(percent, f'Đang convert trang {i}-{last_page} / {total_pages}')
            
            pages = convert_from_path(pdf_path, first_page=i, last_page=last_page)
            
            for idx, page in enumerate(pages):
                page_num = i + idx
                img_filename = f"{page_num:04d}_page.png"
                save_path = os.path.join(abs_folder_path, img_filename)
                
                # Convert image to bytes
                img_byte_arr = io.BytesIO()
                page.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                # Save encrypted
                self.encryption_service.save_encrypted(img_bytes, save_path)
                
                db_session.add(ImageFile(filename=img_filename, album_id=new_album.id))
            
            db_session.commit()
        
        return new_album
