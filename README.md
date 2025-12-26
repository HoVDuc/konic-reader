# 📚 Comic Album Manager

[🇻🇳 Tiếng Việt](README.vi.md)

A Flask web application for managing and viewing comics/image albums with encryption security.

## ✨ Key Features

- **📤 Multiple Upload Formats**: Support for image folders, PDF files, and ZIP archives
- **🔐 Encrypted Storage**: All images are encrypted using Fernet (AES-128-CBC)
- **📖 Series Management**: Organize albums/chapters into series
- **🏷️ Tags & Favorites**: Tag and bookmark albums/series for easy access
- **🖼️ Image Viewer**: Smooth viewing experience with auto-hiding header on scroll
- **👤 User Authentication**: Login system with "Remember Me" functionality
- **📱 Responsive Design**: Mobile-friendly interface

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: SQLite
- **Encryption**: Fernet (cryptography library)
- **PDF Processing**: pdf2image + poppler-utils
- **Frontend**: Jinja2 templates, CSS, JavaScript

## 🏗️ Project Structure

```
comic-album-manager/
├── app/                          # Main Flask application
│   ├── __init__.py               # Application factory
│   ├── models/                   # Database models (SQLAlchemy)
│   │   ├── comic_series.py       # ComicSeries model
│   │   ├── image_album.py        # ImageAlbum model
│   │   ├── image_file.py         # ImageFile model
│   │   ├── user.py               # User model
│   │   └── tag.py                # Tag model
│   ├── routes/                   # Route blueprints
│   │   ├── main.py               # Home page
│   │   ├── auth.py               # Authentication (login/signup/logout)
│   │   ├── upload.py             # File/folder upload
│   │   ├── series.py             # Series management
│   │   ├── album.py              # Album management
│   │   ├── tags.py               # Tags management
│   │   └── api.py                # REST API endpoints
│   ├── services/                 # Business logic
│   │   ├── encryption.py         # File encryption/decryption
│   │   ├── image_service.py      # Image processing
│   │   ├── pdf_processor.py      # PDF file processing
│   │   └── zip_processor.py      # ZIP file processing
│   ├── utils/                    # Utilities
│   │   ├── sorting.py            # Natural sorting
│   │   └── validators.py         # Data validation
│   ├── templates/                # Jinja2 templates
│   │   ├── index.html            # Home page
│   │   ├── login.html            # Login page
│   │   ├── signup.html           # Signup page
│   │   ├── upload.html           # Upload page
│   │   ├── details.html          # Album details
│   │   ├── tags.html             # Tags management
│   │   └── viewer.html           # Image viewer
│   └── static/                   # CSS, JS, assets
│
├── config/                       # Application configuration
│   ├── base.py                   # Base config
│   ├── development.py            # Development config
│   ├── production.py             # Production config
│   └── testing.py                # Testing config
│
├── data/                         # User data (gitignored)
│   ├── albums/                   # Encrypted albums
│   ├── covers/                   # Cover images
│   ├── uploads/                  # Temporary uploads
│   └── instance/                 # SQLite database
│
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
├── tests/                        # Unit tests
│
├── run.py                        # Application entry point
├── init_db.py                    # Database initialization
├── pyproject.toml                # Python dependencies
├── secret.key                    # Encryption key (auto-generated)
└── .env.example                  # Environment variables template
```

## 🚀 Installation & Setup

### Requirements
- Python >= 3.12
- poppler-utils (for PDF processing)

### Installation

```bash
# Clone and enter directory
git clone <repository-url>
cd comic-album-manager

# Install dependencies (with uv - recommended)
uv sync

# Or with pip
pip install -e .

# Install poppler (for PDF processing)
sudo apt install poppler-utils  # Ubuntu/Debian
brew install poppler            # macOS
```

### Running the Application

```bash
# Development mode
python run.py

# Or with Flask CLI
flask run --host=0.0.0.0 --port=5000
```

Access the app at: http://localhost:5000

## 📦 Database Models

### User
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `username` | String(80) | Unique username |
| `password_hash` | String(256) | Hashed password |

### ComicSeries
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(300) | Series name |
| `cover_image` | String(300) | Cover image path |
| `is_completed` | Boolean | Completion status |
| `is_favorite` | Boolean | Favorite flag |
| `albums` | Relationship | List of albums |
| `tags` | Relationship | List of tags |

### ImageAlbum
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(300) | Album/chapter name |
| `folder_path` | String(300) | Folder path |
| `cover_image` | String(300) | Cover image path |
| `series_id` | FK | Parent series |
| `is_favorite` | Boolean | Favorite flag |
| `tags` | Relationship | List of tags |

### Tag
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(50) | Tag name |

### ImageFile
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `filename` | String | Filename |
| `album_id` | FK | Parent album |

## 🔐 Security

- All images are encrypted with **Fernet (AES-128-CBC)**
- Encryption key stored in `secret.key` (auto-generated on first run)
- Images are decrypted only when served to the client
- User passwords are hashed before storage
- "Remember Me" feature uses secure session cookies
- **⚠️ Important**: Backup your `secret.key` - losing it means losing all encrypted data!

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page (Library) |
| GET | `/login` | Login page |
| POST | `/login` | Authenticate user |
| GET | `/signup` | Signup page |
| POST | `/signup` | Register new user |
| GET | `/logout` | Logout user |
| GET | `/upload/` | Upload page |
| GET | `/tags/` | Tags management |
| GET | `/album/<id>` | Album details |
| GET | `/viewer/<id>` | Image viewer |
| POST | `/upload/folder` | Upload image folder |
| POST | `/upload/pdf` | Upload PDF file |
| POST | `/upload/zip` | Upload ZIP file |
| GET | `/api/image/<album_id>/<filename>` | Get image (decrypted) |
| GET | `/series/<id>` | Series details |
| POST | `/series/create` | Create new series |
| POST | `/album/toggle_favorite/<type>/<id>` | Toggle favorite |
| POST | `/album/add_tag/<type>/<id>` | Add tag |
| POST | `/album/remove_tag/<type>/<id>` | Remove tag |

## 📝 Configuration

Create `.env` file from template:

```bash
cp .env.example .env
```

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `DATABASE_URL` | Database connection | sqlite:///data/instance/database.db |
| `FLASK_ENV` | Environment | development |

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

## 📋 Usage Workflow

1. **Register/Login**: Create an account or login (check "Remember Me" to stay logged in)
2. **Upload album**: Go to Upload → Choose type (folder/PDF/ZIP)
3. **Create series**: Go to Upload → Create Series → Enter name
4. **Assign album to series**: Album details → Select series
5. **Manage Tags**: Go to Tags page to edit/delete, or add tags directly in details page
6. **Favorites**: Click star icon to add to favorites list
7. **View content**: Click album → Viewer (Header hides on scroll, Home button to return)

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database error | Delete `data/instance/database.db`, restart app |
| Import error | Run from project root directory |
| PDF not converting | Install `poppler-utils` |
| Images not displaying | Check `secret.key` exists and is unchanged |
| Login issues | Clear browser cookies, try again |

## 📄 License

MIT License
