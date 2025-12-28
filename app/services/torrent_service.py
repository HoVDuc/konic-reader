"""Torrent Service - Handle torrent downloads and imports"""
import os
import time
import shutil
import libtorrent as lt
from werkzeug.utils import secure_filename


class TorrentService:
    """Handles torrent downloading and album creation"""
    
    def __init__(self, app_config):
        self.config = app_config
    
    def download_torrent(self, torrent_file_path, download_path, progress_callback=None):
        """
        Download file from torrent
        
        Args:
            torrent_file_path: Path to .torrent file
            download_path: Directory to save downloaded files
            progress_callback: Optional callback function(percent, message)
        
        Returns:
            Path to downloaded folder or None if error
        """
        if not os.path.exists(torrent_file_path):
            raise FileNotFoundError(f"Torrent file not found: {torrent_file_path}")
        
        # Create session
        ses = lt.session()
        ses.listen_on(6881, 6891)
        
        # Read torrent info
        info = lt.torrent_info(torrent_file_path)
        
        # Add torrent to session
        h = ses.add_torrent({
            'ti': info,
            'save_path': download_path
        })
        
        torrent_name = h.name()
        
        if progress_callback:
            progress_callback(0, f'Đang tải: {torrent_name}')
        
        # Monitor download progress
        state_str = ['queued', 'checking', 'downloading metadata',
                     'downloading', 'finished', 'seeding', 'allocating']
        
        while not h.is_seed():
            s = h.status()
            
            if progress_callback:
                progress_callback(
                    s.progress * 100,
                    f'{state_str[s.state]} - {s.download_rate / 1000:.1f} kB/s - Peers: {s.num_peers}'
                )
            
            time.sleep(1)
        
        if progress_callback:
            progress_callback(100, 'Download hoàn tất!')
        
        # Return the path to downloaded folder
        downloaded_path = os.path.join(download_path, torrent_name)
        return downloaded_path
    
    def import_from_torrent(self, torrent_file, db_session, image_service, progress_callback=None):
        """
        Download torrent and import as album(s)
        
        Args:
            torrent_file: .torrent file object from Flask request
            db_session: Database session
            image_service: ImageService instance
            progress_callback: Optional callback function(percent, message)
        
        Returns:
            List of created albums
        """
        # Save torrent file temporarily
        temp_dir = self.config.get('UPLOAD_FOLDER', '/tmp')
        os.makedirs(temp_dir, exist_ok=True)
        
        torrent_filename = secure_filename(torrent_file.filename)
        temp_torrent_path = os.path.join(temp_dir, torrent_filename)
        torrent_file.save(temp_torrent_path)
        
        # Create download directory
        download_dir = os.path.join(temp_dir, f'torrent_download_{int(time.time())}')
        os.makedirs(download_dir, exist_ok=True)
        
        try:
            # Download torrent
            def download_progress(percent, message):
                if progress_callback:
                    # Map download progress to 0-70%
                    progress_callback(percent * 0.7, message)
            
            downloaded_path = self.download_torrent(
                temp_torrent_path,
                download_dir,
                download_progress
            )
            
            if progress_callback:
                progress_callback(70, 'Đang import ảnh...')
            
            # Check if downloaded path is a folder or file
            created_albums = []
            
            if os.path.isdir(downloaded_path):
                # Import as folder(s)
                created_albums = self._import_folder_structure(
                    downloaded_path,
                    db_session,
                    image_service,
                    progress_callback
                )
            else:
                # Single file (not supported yet)
                raise ValueError("Torrent phải chứa folder với ảnh")
            
            if progress_callback:
                progress_callback(100, 'Hoàn tất!')
            
            return created_albums
            
        finally:
            # Cleanup
            if os.path.exists(temp_torrent_path):
                os.remove(temp_torrent_path)
            if os.path.exists(download_dir):
                shutil.rmtree(download_dir)
    
    def _import_folder_structure(self, root_path, db_session, image_service, progress_callback=None):
        """Import folder structure as albums"""
        from app.models import ImageAlbum, ImageFile
        from PIL import Image
        import io
        
        created_albums = []
        
        # Check if root contains images directly or has subfolders
        has_images_in_root = any(
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
            for f in os.listdir(root_path)
            if os.path.isfile(os.path.join(root_path, f))
        )
        
        if has_images_in_root:
            # Import root as single album
            album = self._create_album_from_folder(
                root_path,
                os.path.basename(root_path),
                db_session,
                image_service
            )
            created_albums.append(album)
        else:
            # Import each subfolder as album
            subfolders = [
                f for f in os.listdir(root_path)
                if os.path.isdir(os.path.join(root_path, f))
            ]
            
            for i, subfolder in enumerate(subfolders):
                subfolder_path = os.path.join(root_path, subfolder)
                
                if progress_callback:
                    percent = 70 + (30 * (i + 1) / len(subfolders))
                    progress_callback(percent, f'Import: {subfolder}')
                
                album = self._create_album_from_folder(
                    subfolder_path,
                    subfolder,
                    db_session,
                    image_service
                )
                created_albums.append(album)
        
        return created_albums
    
    def _create_album_from_folder(self, folder_path, folder_name, db_session, image_service):
        """Create album from folder"""
        from app.models import ImageAlbum, ImageFile
        from PIL import Image
        import io
        
        # Get all image files
        image_files = sorted([
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and
            f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
        ])
        
        if not image_files:
            return None
        
        # Create album
        safe_folder_name = secure_filename(folder_name) + "_" + str(int(time.time()))
        abs_folder_path = os.path.join(self.config['ALBUM_FOLDER'], safe_folder_name)
        os.makedirs(abs_folder_path)
        
        new_album = ImageAlbum(name=folder_name, folder_path=safe_folder_name)
        db_session.add(new_album)
        db_session.commit()
        
        # Process images
        encryption_service = image_service.encryption_service
        
        for idx, img_filename in enumerate(image_files, 1):
            img_path = os.path.join(folder_path, img_filename)
            
            name_without_ext = os.path.splitext(img_filename)[0]
            final_filename = f"{idx:04d}_{secure_filename(name_without_ext)}.webp"
            save_path = os.path.join(abs_folder_path, final_filename)
            
            try:
                # Convert to WebP and encrypt
                img = Image.open(img_path)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='WEBP', quality=90)
                img_data = img_byte_arr.getvalue()
                
                encryption_service.save_encrypted(img_data, save_path)
                
                img_record = ImageFile(filename=final_filename, album_id=new_album.id)
                db_session.add(img_record)
            except Exception as e:
                print(f"Error processing image {img_filename}: {e}")
                continue
        
        db_session.commit()
        time.sleep(0.01)  # Small delay for unique timestamps
        
        return new_album
