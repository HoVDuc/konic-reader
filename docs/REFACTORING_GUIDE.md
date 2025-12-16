# REFACTORING GUIDE

## Overview
This guide explains the complete refactoring process for the albumman project.

## Quick Start

Run the complete refactoring with one command:
```bash
python3 execute_refactor.py
```

This will:
1. Create new directory structure
2. Move existing data to `data/` folder
3. Extract models, services, routes into separate modules
4. Create configuration files
5. Set up project files (.gitignore, README, run.py)

## Manual Execution (Step-by-Step)

If you prefer to run each step manually:

```bash
# Step 1: Create structure
python3 refactor_step1.py

# Step 2: Create models
python3 refactor_step2_models.py

# Step 3: Create services
python3 refactor_step3_services.py

# Step 4: Create utilities
python3 refactor_step4_utils.py

# Step 5: Create configuration
python3 refactor_step5_config.py

# Step 6: Create routes (part 1)
python3 refactor_step6a_routes.py

# Step 7: Create routes (part 2 - uploads)
python3 refactor_step6b_upload.py

# Step 8: Create remaining routes
python3 refactor_step7_remaining_routes.py
```

## After Refactoring

### 1. Create Templates

You need to extract the HTML templates from the old `app.py` or `main.py` files.

Create these files in `app/templates/`:
- `base.html` - Base template with common HTML structure
- `index.html` - Homepage (from TEMPLATE_HOME)
- `details.html` - Album/Series details (from TEMPLATE_DETAILS)
- `viewer.html` - Image viewer (from TEMPLATE_VIEWER)

### 2. Move Static Assets

If you have CSS/JS in the HTML templates:
- Extract CSS → `app/static/css/style.css`
- Extract JS → `app/static/js/upload.js`

### 3. Test the Application

```bash
# Run the new application
python3 run.py

# Visit http://localhost:5000
```

### 4. Verify Functionality

Test each feature:
- [ ] Homepage loads with albums and series
- [ ] Upload PDF works
- [ ] Upload ZIP works  
- [ ] Upload folder works
- [ ] Create series works
- [ ] View album in reader works
- [ ] Album details page works
- [ ] Series details page works
- [ ] Cover image upload works
- [ ] Rename album/series works
- [ ] Delete album/series works
- [ ] Add album to series works
- [ ] Remove album from series works

### 5. Clean Up Old Files

Once everything works, you can remove:
- `app.py` (old monolithic file)
- `main.py` (if it's a duplicate)
- `refactor_step*.py` (refactoring scripts)
- `execute_refactor.py`
- `create_structure.py`
- `setup_structure.py`

Keep:
- `run.py` (new entry point)
- All files in `app/`, `config/`, `data/` directories

## New Project Structure

```
albumman/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   │   ├── comic_series.py
│   │   ├── image_album.py
│   │   └── image_file.py
│   ├── routes/              # Blueprints
│   │   ├── main.py         # Homepage
│   │   ├── upload.py       # File uploads
│   │   ├── series.py       # Series management
│   │   ├── album.py        # Album operations
│   │   └── api.py          # JSON APIs
│   ├── services/            # Business logic
│   │   ├── encryption.py
│   │   ├── pdf_processor.py
│   │   ├── zip_processor.py
│   │   └── image_service.py
│   ├── utils/               # Helpers
│   │   ├── sorting.py
│   │   └── validators.py
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── details.html
│   │   └── viewer.html
│   └── static/              # CSS, JS, images
│       ├── css/
│       ├── js/
│       └── img/
├── config/                  # Configuration
│   ├── base.py
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── data/                    # User data (gitignored)
│   ├── uploads/
│   ├── albums/
│   ├── covers/
│   └── instance/
├── tests/                   # Test suite
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Dependencies
├── README.md               # Project info
└── run.py                  # Entry point
```

## Key Changes

### Before (Monolithic)
- Single 600+ line file
- HTML in Python strings
- All logic mixed together
- Hard-coded configuration

### After (Modular)
- Organized by concern
- Proper MVC separation
- Reusable services
- Environment-based config
- Easy to test
- Easy to extend

## Benefits

1. **Maintainability**: Each file has a single responsibility
2. **Scalability**: Easy to add new features
3. **Testability**: Can test each component in isolation
4. **Collaboration**: Multiple developers can work simultaneously
5. **Best Practices**: Follows Flask application factory pattern
6. **Security**: Config via environment variables

## Troubleshooting

### Templates not found
- Make sure you extracted HTML to `app/templates/`
- Check template names match what routes expect

### Import errors
- Verify all `__init__.py` files exist
- Check circular imports

### Database errors
- Delete old `database.db` and let it recreate
- Check `data/instance/` directory exists

### 404 errors
- Verify blueprint registration in `app/__init__.py`
- Check route URL prefixes

## Next Steps

1. Add tests in `tests/` directory
2. Add documentation in `docs/`
3. Consider adding:
   - User authentication
   - API rate limiting
   - Caching layer
   - Background task queue (Celery)
   - Docker containerization

## Support

If you encounter issues:
1. Check the error logs
2. Verify all files were created
3. Ensure dependencies are installed
4. Review this guide

Happy coding! 🎉
