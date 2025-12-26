# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Comic Album Manager is a Flask web application for managing and viewing comic albums/image collections with AES encryption. All uploaded images are encrypted using Fernet (AES-128-CBC) and stored securely. The application supports uploading folders, PDFs, and ZIP files, which are converted and encrypted automatically.

## Development Commands

### Running the Application

```bash
# Development server with debug mode
python run.py

# Alternative: Using Flask CLI
flask run --host=0.0.0.0 --port=5000
```

The application runs on `http://localhost:5000` by default.

### Database Management

```bash
# Initialize/recreate database tables
python init_db.py

# Note: Database is automatically created on first run via app factory
```

Database file location: `data/instance/database.db` (SQLite)

### Dependencies

```bash
# Install with uv (recommended)
uv sync

# Install with pip
pip install -e .

# System dependencies for PDF processing
sudo apt install poppler-utils  # Ubuntu/Debian
brew install poppler            # macOS
```

### Testing

The `tests/` directory exists but currently has no test files. When adding tests:

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

## Architecture

### Application Factory Pattern

The app uses Flask's application factory pattern (`app/__init__.py`):
- Configuration is loaded based on environment (development/production)
- Database and extensions are initialized via `db.init_app(app)`
- Blueprints are registered after initialization
- Database tables are auto-created on app context creation

### Key Architectural Components

#### 1. Encryption Layer (`app/services/encryption.py`)

All images pass through the encryption service:
- **Encryption key**: Stored in `secret.key` at project root (auto-generated if missing)
- **CRITICAL**: Loss of `secret.key` means permanent data loss - all encrypted images become unrecoverable
- Uses Fernet symmetric encryption (AES-128-CBC with HMAC)
- Images are encrypted before storage and decrypted on-demand when serving

#### 2. Processing Services (`app/services/`)

Three main processors handle different upload types:
- **PDFProcessor**: Converts PDF pages to WebP images using `pdf2image`, encrypts and stores them
- **ZIPProcessor**: Extracts images from ZIP archives, converts to WebP, encrypts and stores
- **ImageService**: Processes folder uploads, converts various image formats to WebP

All processors:
- Convert images to WebP format for consistency and compression
- Use background threading for long-running operations (PDF/ZIP)
- Report progress via callback functions to API endpoints
- Generate sequential filenames (0001_*.webp, 0002_*.webp, etc.)

#### 3. Database Models (`app/models/`)

Hierarchical structure:
- **ComicSeries** (parent) → **ImageAlbum** (child) → **ImageFile** (child)
- **Tag**: Many-to-many relationships with both Series and Albums via association tables
- Albums can exist independently without a series (`series_id` nullable)

Key relationships:
```
ComicSeries (1) ──< (N) ImageAlbum (1) ──< (N) ImageFile
     │                      │
     └──< (N:M) Tag (N:M) >─┘
```

#### 4. Blueprint Organization (`app/routes/`)

Routes are organized by domain:
- **main_bp** (`/`): Library homepage, displays all series and standalone albums
- **upload_bp** (`/upload/`): Upload page and handlers for folder/PDF/ZIP uploads
- **series_bp** (`/series/`): Series creation and management
- **album_bp** (`/album/`): Album viewer, details page, image serving, rename/delete operations
- **tags_bp** (`/tags/`): Tag management interface
- **api_bp** (`/api/`): Background task progress tracking

#### 5. Image Serving Flow

Critical path for viewing images:
1. User requests `/album/<id>` → renders viewer with list of encrypted filenames
2. Browser requests `/api/image/<album_id>/<filename>`
3. `album.get_image()` route:
   - Looks up album and constructs file path
   - Passes encrypted file to `EncryptionService.get_decrypted_file()`
   - Returns decrypted image bytes with correct MIME type
   - Image is never stored decrypted on disk

### Configuration System (`config/`)

Three-tier configuration:
- **BaseConfig**: Shared settings (paths, encryption key location, upload limits)
- **DevelopmentConfig**: DEBUG=True, SQLite database, no SQL echo by default
- **ProductionConfig**: Production-ready settings (should set proper SECRET_KEY)

Directories defined in `BaseConfig`:
- `DATA_DIR/albums/`: Encrypted album folders
- `DATA_DIR/covers/`: Cover images (stored unencrypted)
- `DATA_DIR/uploads/`: Temporary upload staging
- `DATA_DIR/instance/`: SQLite database location

## Important Patterns

### Natural Sorting

The codebase uses `natural_sort_key()` from `app/utils/sorting.py` for human-friendly sorting:
- Used for album lists within a series
- Used for file ordering during uploads
- Handles numeric sequences correctly (e.g., "Chapter 2" before "Chapter 10")

### Progress Tracking for Background Tasks

PDF and ZIP uploads use threading with shared progress state:
- Task IDs generated using `uuid.uuid4()`
- Progress stored in `conversion_progress` dict in `app/routes/api.py`
- Frontend polls `/api/status/<task_id>` for updates
- Progress callbacks update percent complete and status message

### File Naming Convention

Processed images follow a strict naming pattern:
- Format: `{sequence:04d}_{original_name}.webp`
- Example: `0001_page.webp`, `0042_cover.webp`
- Ensures consistent ordering and format

## Security Considerations

- **Encryption key management**: The `secret.key` file must be backed up and never committed to version control
- **Session security**: Flask SECRET_KEY should be changed in production (set via environment variable)
- **File upload limits**: 500 MB max upload size set in `BaseConfig.MAX_CONTENT_LENGTH`
- **Cover images**: Stored unencrypted in `data/covers/` (considered public preview images)

## Data Directory Structure

```
data/
├── albums/          # Encrypted album folders (gitignored)
│   └── {album_folder_name}/
│       ├── 0001_*.webp
│       └── 0002_*.webp
├── covers/          # Unencrypted cover images (gitignored)
├── uploads/         # Temporary upload staging (gitignored)
└── instance/        # SQLite database (gitignored)
    └── database.db
```

## Common Operations

### Adding a New Route

1. Create route function in appropriate blueprint file (`app/routes/`)
2. Use existing patterns: `@blueprint_name.route('/path', methods=['GET', 'POST'])`
3. Import required models from `app.models`
4. Commit database changes with `db.session.commit()`
5. Blueprint is auto-registered in `app/__init__.py`

### Adding a New Service

1. Create service class in `app/services/`
2. Accept `app_config` and `encryption_service` in `__init__` if needed
3. Follow existing patterns from `PDFProcessor`, `ZIPProcessor`, or `ImageService`
4. Import and instantiate in routes using `get_services()` helper

### Modifying Database Schema

1. Update model classes in `app/models/`
2. For development: Delete `data/instance/database.db` and run `python init_db.py`
3. For production: Implement proper migrations (currently no migration system in place)

## Troubleshooting

- **Import errors**: Always run commands from project root directory
- **Database errors**: Delete `data/instance/database.db` and re-initialize
- **Images not displaying**: Verify `secret.key` exists and hasn't been changed/corrupted
- **PDF conversion fails**: Ensure `poppler-utils` is installed system-wide
- **Background tasks stuck**: Check console output for exceptions in worker threads
