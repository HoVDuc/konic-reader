#!/usr/bin/env python3
"""Check all albums and files"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.models import ImageAlbum, ImageFile

app = create_app()

with app.app_context():
    albums = ImageAlbum.query.all()
    print(f"\n=== Total Albums: {len(albums)} ===\n")
    
    for album in albums:
        images = ImageFile.query.filter_by(album_id=album.id).all()
        print(f"Album #{album.id}: {album.name}")
        print(f"  Folder: {album.folder_path}")
        print(f"  Images ({len(images)}):")
        for img in images[:10]:  # First 10 files
            print(f"    - {img.filename}")
        if len(images) > 10:
            print(f"    ... and {len(images) - 10} more")
        print()
