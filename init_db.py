#!/usr/bin/env python3
"""
Database initialization script
Run this if you have database issues
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Initializing database...")

from app import create_app, db
from app.models import ComicSeries, ImageAlbum, ImageFile

app = create_app('development')

with app.app_context():
    # Drop all tables (careful!)
    print("Creating tables...")
    db.create_all()
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"\n✓ Tables created: {tables}")
    
    # Check for existing data
    series_count = ComicSeries.query.count()
    album_count = ImageAlbum.query.count()
    
    print(f"\n✓ Existing data:")
    print(f"  - Series: {series_count}")
    print(f"  - Albums: {album_count}")
    
    print("\n✓ Database ready!")
