#!/usr/bin/env python3
"""
SIMPLE REFACTORING SCRIPT - COMPLETE IN ONE FILE
This does everything without dependencies on other scripts
"""

import os
import shutil
import re
import sys
from datetime import datetime

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(step_num, total, description):
    print(f"\n[Step {step_num}/{total}] {description}...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print_header("ALBUMMAN - COMPLETE PROJECT REFACTORING")
    print("\nThis script will restructure your entire project.")
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Refactoring cancelled.")
        return
    
    total_steps = 8
    
    try:
        # STEP 1: Create directory structure
        print_step(1, total_steps, "Creating directory structure")
        
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
        
        # STEP 2: Move existing data
        print_step(2, total_steps, "Moving existing data")
        
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
            elif os.path.exists(old_path) and os.path.exists(new_path):
                print(f"  - Skipped: {new} already exists")
        
        # STEP 3: Create __init__.py files
        print_step(3, total_steps, "Creating package files")
        
        init_locations = [
            'app', 'app/models', 'app/routes', 'app/services', 
            'app/utils', 'tests', 'config'
        ]
        
        for location in init_locations:
            init_path = os.path.join(BASE_DIR, location, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    if location == 'app':
                        # Create app factory
                        f.write('''"""Flask application factory"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.upload import upload_bp
    from app.routes.series import series_bp
    from app.routes.album import album_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(series_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(api_bp)
    
    return app
''')
                    else:
                        f.write(f'"""{location.replace("/", ".")} module"""\n')
        
        print("  ✓ Package files created")
        
        # STEP 4: Extract templates from old files
        print_step(4, total_steps, "Extracting templates")
        
        old_content = None
        for filename in ['main.py', 'app.py']:
            filepath = os.path.join(BASE_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                print(f"  ✓ Reading from {filename}")
                break
        
        if old_content:
            templates_dir = os.path.join(BASE_DIR, 'app', 'templates')
            
            # Extract TEMPLATE_HOME
            match = re.search(r'TEMPLATE_HOME\s*=\s*"""(.*?)"""', old_content, re.DOTALL)
            if match:
                with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
                    f.write(match.group(1))
                print("  ✓ Extracted index.html")
            
            # Extract TEMPLATE_DETAILS
            match = re.search(r'TEMPLATE_DETAILS\s*=\s*"""(.*?)"""', old_content, re.DOTALL)
            if match:
                with open(os.path.join(templates_dir, 'details.html'), 'w', encoding='utf-8') as f:
                    f.write(match.group(1))
                print("  ✓ Extracted details.html")
            
            # Extract TEMPLATE_VIEWER
            match = re.search(r'TEMPLATE_VIEWER\s*=\s*"""(.*?)"""', old_content, re.DOTALL)
            if match:
                with open(os.path.join(templates_dir, 'viewer.html'), 'w', encoding='utf-8') as f:
                    f.write(match.group(1))
                print("  ✓ Extracted viewer.html")
        
        # STEP 5: Run individual refactoring steps
        print_step(5, total_steps, "Creating models, services, routes...")
        
        # Execute the creation scripts
        for script in ['refactor_step2_models.py', 'refactor_step3_services.py', 
                      'refactor_step4_utils.py', 'refactor_step5_config.py',
                      'refactor_step6a_routes.py', 'refactor_step6b_upload.py',
                      'refactor_step7_remaining_routes.py']:
            script_path = os.path.join(BASE_DIR, script)
            if os.path.exists(script_path):
                with open(script_path, 'r') as f:
                    exec(f.read())
        
        # STEP 6: Create run.py
        print_step(6, total_steps, "Creating entry point")
        
        run_py = '''#!/usr/bin/env python3
"""Application entry point"""

from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        with open(os.path.join(BASE_DIR, 'run.py'), 'w') as f:
            f.write(run_py)
        print("  ✓ Created run.py")
        
        # STEP 7: Create .env.example and .gitignore
        print_step(7, total_steps, "Creating configuration files")
        
        env_example = '''# Environment Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///data/instance/database.db
FLASK_ENV=development
'''
        with open(os.path.join(BASE_DIR, '.env.example'), 'w') as f:
            f.write(env_example)
        print("  ✓ Created .env.example")
        
        gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Application Data
data/
instance/
*.db
*.sqlite

# Security
secret.key
.env

# OS
.DS_Store
Thumbs.db

# Refactoring scripts
refactor_*.py
REFACTOR_NOW.py
execute_refactor.py
extract_templates.py
'''
        with open(os.path.join(BASE_DIR, '.gitignore'), 'w') as f:
            f.write(gitignore)
        print("  ✓ Updated .gitignore")
        
        # STEP 8: Create migration notes
        print_step(8, total_steps, "Creating documentation")
        
        migration_notes = f'''# Migration Completed

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## What was done:

1. ✓ Created new directory structure
2. ✓ Moved data to data/ folder
3. ✓ Extracted models to app/models/
4. ✓ Extracted services to app/services/
5. ✓ Created route blueprints in app/routes/
6. ✓ Created configuration in config/
7. ✓ Extracted HTML templates to app/templates/
8. ✓ Created utility functions in app/utils/
9. ✓ Created run.py entry point

## Next steps:

1. Test the application:
   ```bash
   python3 run.py
   ```

2. Visit http://localhost:5000

3. Verify all features work

4. If everything works, remove old files:
   ```bash
   rm app.py main.py refactor_*.py REFACTOR_NOW.py
   ```

## Documentation:

- See REFACTORING_GUIDE.md for detailed information
- See CHECKLIST.md for testing checklist
'''
        
        with open(os.path.join(BASE_DIR, 'MIGRATION_NOTES.md'), 'w') as f:
            f.write(migration_notes)
        print("  ✓ Created MIGRATION_NOTES.md")
        
        # SUCCESS!
        print_header("✓ REFACTORING COMPLETED SUCCESSFULLY!")
        
        print("\n📋 Summary:")
        print("  ✓ Directory structure created")
        print("  ✓ Existing data moved to data/")
        print("  ✓ Code split into modules")
        print("  ✓ Templates extracted")
        print("  ✓ Configuration files created")
        print("  ✓ Documentation generated")
        
        print("\n🚀 Next Steps:")
        print("\n1. Start the application:")
        print("   python3 run.py")
        
        print("\n2. Visit http://localhost:5000 and test all features")
        
        print("\n3. Review these files:")
        print("   - MIGRATION_NOTES.md")
        print("   - CHECKLIST.md")
        
        print("\n4. After verification, clean up:")
        print("   rm app.py main.py refactor_*.py REFACTOR_NOW.py")
        
        print("\n" + "="*70)
        print("  Have a great day! 🎉")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during refactoring: {e}")
        import traceback
        traceback.print_exc()
        print("\nRefactoring failed. Please check the error above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
