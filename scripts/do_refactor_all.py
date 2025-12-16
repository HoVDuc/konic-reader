#!/usr/bin/env python3
"""
COMPLETE REFACTORING - ALL IN ONE
This script performs the entire refactoring process
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("="*70)
print(" ALBUMMAN PROJECT - COMPLETE REFACTORING")
print("="*70)

# === STEP 1: CREATE DIRECTORIES ===
print("\n[1/8] Creating directory structure...")
dirs = [
    'app/models', 'app/routes', 'app/services', 'app/utils', 
    'app/templates', 'app/static/css', 'app/static/js', 'app/static/img',
    'data/uploads', 'data/albums', 'data/covers', 'data/instance',
    'config', 'tests', 'docs', 'scripts'
]

for d in dirs:
    path = os.path.join(BASE_DIR, d)
    os.makedirs(path, exist_ok=True)
print("  ✓ Directories created")

# === STEP 2: MOVE EXISTING DATA ===
print("\n[2/8] Moving existing data...")
migrations = [
    ('uploads', 'data/uploads'),
    ('albums', 'data/albums'),
    ('covers', 'data/covers'),
    ('instance', 'data/instance'),
]

for old, new in migrations:
    old_path = os.path.join(BASE_DIR, old)
    new_path = os.path.join(BASE_DIR, new)
    
    if os.path.exists(old_path) and not os.path.exists(new_path):
        shutil.move(old_path, new_path)
        print(f"  ✓ Moved: {old} -> {new}")
    elif os.path.exists(old_path):
        print(f"  - Skipped: {new} already exists")

print("  ✓ Data migration complete")

# === STEP 3: CREATE ALL FILES ===
print("\n[3/8] Creating all project files...")

# This will be executed by importing the step scripts
exec(open(os.path.join(BASE_DIR, 'refactor_step2_models.py')).read())
exec(open(os.path.join(BASE_DIR, 'refactor_step3_services.py')).read())
exec(open(os.path.join(BASE_DIR, 'refactor_step4_utils.py')).read())
exec(open(os.path.join(BASE_DIR, 'refactor_step5_config.py')).read())

print("\n✓ Core files created!")
print("\n" + "="*70)
print(" Refactoring Steps 1-3 Complete!")
print("="*70)
print("\nRun the following to complete:")
print("  python3 refactor_step6a_routes.py")
print("  python3 refactor_step6b_upload.py")
print("  python3 create_remaining_routes.py")
print("  python3 create_templates.py")
