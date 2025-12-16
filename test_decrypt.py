#!/usr/bin/env python3
"""Test decryption"""
import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.models import ImageAlbum, ImageFile
from app.services import EncryptionService

app = create_app()

with app.app_context():
    # List all albums
    albums = ImageAlbum.query.all()
    print(f"\n=== Found {len(albums)} albums ===")
    
    for album in albums:
        print(f"\nAlbum ID: {album.id}")
        print(f"Name: {album.name}")
        print(f"Folder: {album.folder_path}")
        
        folder_path = os.path.join(app.config['ALBUM_FOLDER'], album.folder_path)
        print(f"Full path: {folder_path}")
        
        if os.path.exists(folder_path):
            files_on_disk = os.listdir(folder_path)
            print(f"Files on disk: {files_on_disk[:5]}")  # First 5 files
            
            images = ImageFile.query.filter_by(album_id=album.id).all()
            print(f"Files in DB: {len(images)}")
            if images:
                print(f"All files in DB:")
                for img in images:
                    print(f"  - {img.filename}")
                
                # Test if file exists
                test_file = os.path.join(folder_path, images[0].filename)
                if os.path.exists(test_file):
                    print(f"✓ File exists: {images[0].filename}")
                    
                    # Test decryption
                    try:
                        encryption_service = EncryptionService(app.config['KEY_FILE'])
                        decrypted = encryption_service.get_decrypted_file(test_file)
                        data = decrypted.read()
                        print(f"✓ Decryption successful! Size: {len(data)} bytes")
                        
                        # Check if it's valid image
                        if data.startswith(b'\x89PNG'):
                            print("✓ Valid PNG image")
                        elif data.startswith(b'\xff\xd8\xff'):
                            print("✓ Valid JPEG image")
                        else:
                            print(f"⚠ Unknown format, first bytes: {data[:10]}")
                    except Exception as e:
                        print(f"✗ Decryption failed: {e}")
                else:
                    print(f"✗ File not found: {images[0].filename}")
        else:
            print("✗ Folder does not exist!")
