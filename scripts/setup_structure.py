#!/usr/bin/env python3
"""Script to create new directory structure"""

if __name__ == '__main__':
    import os
    import sys
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    base = os.path.dirname(os.path.abspath(__file__))
    
    dirs = [
        'app/models',
        'app/routes', 
        'app/services',
        'app/utils',
        'app/templates',
        'app/static/css',
        'app/static/js', 
        'app/static/img',
        'data/uploads',
        'data/albums',
        'data/covers', 
        'data/instance',
        'config',
        'tests',
        'docs',
        'scripts'
    ]
    
    for d in dirs:
        path = os.path.join(base, d)
        os.makedirs(path, exist_ok=True)
    
    # Create __init__.py files
    init_files = [
        'app/__init__.py',
        'app/models/__init__.py',
        'app/routes/__init__.py',
        'app/services/__init__.py',
        'app/utils/__init__.py',
        'tests/__init__.py',
    ]
    
    for init_file in init_files:
        path = os.path.join(base, init_file)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('')
    
    print('Structure created successfully!')
    
    # Execute the refactoring
    exec(open(os.path.join(base, 'do_refactor.py')).read())
