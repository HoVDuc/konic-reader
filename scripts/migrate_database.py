#!/usr/bin/env python3
"""
Database migration script - Export from old database and import to new database
"""
import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, ComicSeries, ImageAlbum, ImageFile, Tag

def export_database(db_path, export_file):
    """Export all data from database to JSON file"""
    app = create_app()

    with app.app_context():
        print(f"Exporting data from: {db_path}")

        # Check if database exists
        if not os.path.exists(db_path):
            print(f"Database not found: {db_path}")
            return False

        data = {
            'exported_at': datetime.utcnow().isoformat(),
            'version': '1.0',
            'users': [],
            'series': [],
            'albums': [],
            'files': [],
            'tags': [],
            'album_tags': [],
            'series_tags': []
        }

        # Export users
        users = User.query.all()
        for user in users:
            data['users'].append({
                'id': user.id,
                'username': user.username,
                'password_hash': user.password_hash
            })

        # Export tags
        tags = Tag.query.all()
        for tag in tags:
            data['tags'].append({
                'id': tag.id,
                'name': tag.name
            })

        # Export series (use raw SQL to handle missing created_at column)
        series_query = """
        SELECT id, name, cover_image, is_completed, is_favorite
        FROM comic_series
        """
        series_result = db.session.execute(db.text(series_query))
        for row in series_result:
            series_data = {
                'id': row[0],
                'name': row[1],
                'cover_image': row[2],
                'is_completed': row[3],
                'is_favorite': row[4],
                'created_at': datetime.utcnow().isoformat()  # Default for old records
            }
            data['series'].append(series_data)

            # Export series tags (use raw SQL)
            tags_query = """
            SELECT tag_id FROM series_tags WHERE series_id = :series_id
            """
            tags_result = db.session.execute(db.text(tags_query), {'series_id': row[0]})
            for tag_row in tags_result:
                data['series_tags'].append({
                    'series_id': row[0],
                    'tag_id': tag_row[0]
                })

        # Export albums (use raw SQL to handle missing created_at column)
        albums_query = """
        SELECT id, name, folder_path, cover_image, series_id, is_favorite
        FROM image_album
        """
        albums_result = db.session.execute(db.text(albums_query))
        for row in albums_result:
            album_data = {
                'id': row[0],
                'name': row[1],
                'folder_path': row[2],
                'cover_image': row[3],
                'series_id': row[4],
                'is_favorite': row[5],
                'created_at': datetime.utcnow().isoformat()  # Default for old records
            }
            data['albums'].append(album_data)

            # Export album tags (use raw SQL)
            tags_query = """
            SELECT tag_id FROM album_tags WHERE album_id = :album_id
            """
            tags_result = db.session.execute(db.text(tags_query), {'album_id': row[0]})
            for tag_row in tags_result:
                data['album_tags'].append({
                    'album_id': row[0],
                    'tag_id': tag_row[0]
                })

        # Export files
        files = ImageFile.query.all()
        for file in files:
            data['files'].append({
                'id': file.id,
                'filename': file.filename,
                'album_id': file.album_id
            })

        # Save to JSON file
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Exported {len(data['users'])} users")
        print(f"✓ Exported {len(data['series'])} series")
        print(f"✓ Exported {len(data['albums'])} albums")
        print(f"✓ Exported {len(data['files'])} files")
        print(f"✓ Exported {len(data['tags'])} tags")
        print(f"✓ Data saved to: {export_file}")

        return True

def import_database(export_file, db_path):
    """Import data from JSON file to database"""
    app = create_app()

    with app.app_context():
        print(f"Importing data to: {db_path}")

        # Load data from JSON
        if not os.path.exists(export_file):
            print(f"Export file not found: {export_file}")
            return False

        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Importing data exported at: {data.get('exported_at', 'Unknown')}")

        # Clear existing data
        print("Clearing existing data...")
        ImageFile.query.delete()
        db.session.execute(db.text("DELETE FROM album_tags"))
        db.session.execute(db.text("DELETE FROM series_tags"))
        ImageAlbum.query.delete()
        ComicSeries.query.delete()
        Tag.query.delete()
        User.query.delete()
        db.session.commit()

        # Import users
        print(f"Importing {len(data['users'])} users...")
        for user_data in data['users']:
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                password_hash=user_data['password_hash']
            )
            db.session.add(user)
        db.session.commit()

        # Import tags
        print(f"Importing {len(data['tags'])} tags...")
        for tag_data in data['tags']:
            tag = Tag(
                id=tag_data['id'],
                name=tag_data['name']
            )
            db.session.add(tag)
        db.session.commit()

        # Import series
        print(f"Importing {len(data['series'])} series...")
        for series_data in data['series']:
            created_at = datetime.fromisoformat(series_data['created_at'])
            series = ComicSeries(
                id=series_data['id'],
                name=series_data['name'],
                cover_image=series_data['cover_image'],
                is_completed=series_data['is_completed'],
                is_favorite=series_data['is_favorite'],
                created_at=created_at
            )
            db.session.add(series)
        db.session.commit()

        # Import series tags
        print(f"Importing {len(data['series_tags'])} series tags...")
        for st_data in data['series_tags']:
            db.session.execute(
                db.text("INSERT INTO series_tags (series_id, tag_id) VALUES (:series_id, :tag_id)"),
                {'series_id': st_data['series_id'], 'tag_id': st_data['tag_id']}
            )
        db.session.commit()

        # Import albums
        print(f"Importing {len(data['albums'])} albums...")
        for album_data in data['albums']:
            created_at = datetime.fromisoformat(album_data['created_at'])
            album = ImageAlbum(
                id=album_data['id'],
                name=album_data['name'],
                folder_path=album_data['folder_path'],
                cover_image=album_data['cover_image'],
                series_id=album_data['series_id'],
                is_favorite=album_data['is_favorite'],
                created_at=created_at
            )
            db.session.add(album)
        db.session.commit()

        # Import album tags
        print(f"Importing {len(data['album_tags'])} album tags...")
        for at_data in data['album_tags']:
            db.session.execute(
                db.text("INSERT INTO album_tags (album_id, tag_id) VALUES (:album_id, :tag_id)"),
                {'album_id': at_data['album_id'], 'tag_id': at_data['tag_id']}
            )
        db.session.commit()

        # Import files
        print(f"Importing {len(data['files'])} files...")
        for file_data in data['files']:
            file = ImageFile(
                id=file_data['id'],
                filename=file_data['filename'],
                album_id=file_data['album_id']
            )
            db.session.add(file)
        db.session.commit()

        print("✓ Import completed successfully!")
        return True

def backup_files(source_data_dir, backup_dir):
    """Backup album files, covers, etc."""
    if not os.path.exists(source_data_dir):
        print(f"Source data directory not found: {source_data_dir}")
        return False

    print(f"Backing up files from: {source_data_dir}")

    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)

    # Copy directories
    dirs_to_backup = ['albums', 'covers', 'uploads']
    for dir_name in dirs_to_backup:
        src_dir = os.path.join(source_data_dir, dir_name)
        dst_dir = os.path.join(backup_dir, dir_name)

        if os.path.exists(src_dir):
            print(f"Copying {dir_name}...")
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"✓ Backed up {dir_name}")
        else:
            print(f"⚠ {dir_name} directory not found, skipping")

    return True

def restore_files(backup_dir, target_data_dir):
    """Restore album files, covers, etc."""
    if not os.path.exists(backup_dir):
        print(f"Backup directory not found: {backup_dir}")
        return False

    print(f"Restoring files to: {target_data_dir}")

    # Create target directory
    os.makedirs(target_data_dir, exist_ok=True)

    # Copy directories
    dirs_to_restore = ['albums', 'covers', 'uploads']
    for dir_name in dirs_to_restore:
        src_dir = os.path.join(backup_dir, dir_name)
        dst_dir = os.path.join(target_data_dir, dir_name)

        if os.path.exists(src_dir):
            print(f"Restoring {dir_name}...")
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"✓ Restored {dir_name}")
        else:
            print(f"⚠ {dir_name} not found in backup, skipping")

    return True

def main():
    """Main migration function"""
    import argparse

    parser = argparse.ArgumentParser(description='Database migration tool')
    parser.add_argument('action', choices=['export', 'import', 'backup', 'restore', 'full-migrate'],
                       help='Action to perform')
    parser.add_argument('--old-db', help='Path to old database file')
    parser.add_argument('--new-db', help='Path to new database file')
    parser.add_argument('--export-file', default='database_export.json',
                       help='Export file path (default: database_export.json)')
    parser.add_argument('--backup-dir', default='data_backup',
                       help='Backup directory (default: data_backup)')
    parser.add_argument('--old-data-dir', help='Old data directory path')
    parser.add_argument('--new-data-dir', help='New data directory path')

    args = parser.parse_args()

    # Set default paths
    project_root = Path(__file__).parent.parent
    default_old_db = project_root / 'data' / 'instance' / 'database.db'
    default_new_db = project_root / 'data' / 'instance' / 'database.db'
    default_old_data = project_root / 'data'
    default_new_data = project_root / 'data'

    old_db = args.old_db or str(default_old_db)
    new_db = args.new_db or str(default_new_db)
    old_data_dir = args.old_data_dir or str(default_old_data)
    new_data_dir = args.new_data_dir or str(default_new_data)

    if args.action == 'export':
        success = export_database(old_db, args.export_file)
        if success:
            print(f"\n✅ Export completed! File saved to: {args.export_file}")
        else:
            print("\n❌ Export failed!")
            sys.exit(1)

    elif args.action == 'import':
        success = import_database(args.export_file, new_db)
        if success:
            print(f"\n✅ Import completed! Database updated: {new_db}")
        else:
            print("\n❌ Import failed!")
            sys.exit(1)

    elif args.action == 'backup':
        success = backup_files(old_data_dir, args.backup_dir)
        if success:
            print(f"\n✅ Backup completed! Files saved to: {args.backup_dir}")
        else:
            print("\n❌ Backup failed!")
            sys.exit(1)

    elif args.action == 'restore':
        success = restore_files(args.backup_dir, new_data_dir)
        if success:
            print(f"\n✅ Restore completed! Files restored to: {new_data_dir}")
        else:
            print("\n❌ Restore failed!")
            sys.exit(1)

    elif args.action == 'full-migrate':
        print("🚀 Starting full migration...")

        # Step 1: Export data
        print("\n📤 Step 1: Exporting data...")
        if not export_database(old_db, args.export_file):
            print("❌ Export failed!")
            sys.exit(1)

        # Step 2: Backup files
        print("\n💾 Step 2: Backing up files...")
        if not backup_files(old_data_dir, args.backup_dir):
            print("❌ Backup failed!")
            sys.exit(1)

        # Step 3: Import data
        print("\n📥 Step 3: Importing data...")
        if not import_database(args.export_file, new_db):
            print("❌ Import failed!")
            sys.exit(1)

        # Step 4: Restore files
        print("\n🔄 Step 4: Restoring files...")
        if not restore_files(args.backup_dir, new_data_dir):
            print("❌ Restore failed!")
            sys.exit(1)

        print("\n🎉 Full migration completed successfully!")
        print(f"📄 Export file: {args.export_file}")
        print(f"💾 Backup directory: {args.backup_dir}")
        print(f"🗄️ New database: {new_db}")
        print(f"📁 Restored files: {new_data_dir}")

if __name__ == '__main__':
    main()