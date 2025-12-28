#!/usr/bin/env python3
"""
Test script to verify database migration
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        from app import create_app
        from app.models import db

        app = create_app()
        with app.app_context():
            # Test database connection
            db.engine.execute(db.text('SELECT 1'))
            print("✓ Database connection successful")

            # Check tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Found tables: {tables}")

            # Check if required tables exist
            required_tables = ['user', 'comic_series', 'image_album', 'image_file', 'tag']
            for table in required_tables:
                if table in tables:
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' missing")

            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test if models can be imported and used"""
    try:
        from app.models import User, ComicSeries, ImageAlbum, ImageFile, Tag

        # Test model creation
        user = User(username="test", password_hash="test")
        series = ComicSeries(name="Test Series")
        album = ImageAlbum(name="Test Album", folder_path="/test")
        file = ImageFile(filename="test.jpg", album_id=1)
        tag = Tag(name="test tag")

        print("✓ All models can be instantiated")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing database setup...\n")

    # Test 1: Database connection
    print("1. Testing database connection:")
    db_ok = test_database_connection()
    print()

    # Test 2: Models
    print("2. Testing models:")
    models_ok = test_models()
    print()

    # Summary
    if db_ok and models_ok:
        print("🎉 All tests passed! Database is ready for migration.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)