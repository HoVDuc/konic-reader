#!/usr/bin/env python3
import os

base = '/home/anlab/hovduc/albumman'
dirs = [
    'app/models', 'app/routes', 'app/services', 'app/utils', 
    'app/templates', 'app/static/css', 'app/static/js', 'app/static/img',
    'data/uploads', 'data/albums', 'data/covers', 'data/instance',
    'config', 'tests', 'docs', 'scripts'
]

for d in dirs:
    path = os.path.join(base, d)
    os.makedirs(path, exist_ok=True)
    print(f'Created: {path}')

print('\nAll directories created successfully!')
