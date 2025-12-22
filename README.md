# 📚 Comic Album Manager

Ứng dụng web Flask để quản lý và xem truyện tranh/album ảnh với tính năng mã hóa bảo mật.

## ✨ Tính năng chính

- **📤 Upload đa dạng**: Hỗ trợ upload folder ảnh, file PDF, file ZIP
- **🔐 Mã hóa bảo mật**: Tất cả ảnh được mã hóa với Fernet (AES-128)
- **📖 Quản lý Series**: Nhóm các album/chapter thành series
- **🖼️ Viewer ảnh**: Xem ảnh với giao diện thân thiện
- **📱 Responsive**: Giao diện tương thích mobile

## 🏗️ Cấu trúc dự án

```
comic-album-manager/
├── app/                          # Ứng dụng Flask chính
│   ├── __init__.py               # Application factory
│   ├── models/                   # Database models (SQLAlchemy)
│   │   ├── comic_series.py       # Model ComicSeries
│   │   ├── image_album.py        # Model ImageAlbum
│   │   └── image_file.py         # Model ImageFile
│   ├── routes/                   # Route blueprints
│   │   ├── main.py               # Trang chủ
│   │   ├── upload.py             # Upload file/folder
│   │   ├── series.py             # Quản lý series
│   │   ├── album.py              # Quản lý album
│   │   └── api.py                # REST API endpoints
│   ├── services/                 # Business logic
│   │   ├── encryption.py         # Mã hóa/giải mã file
│   │   ├── image_service.py      # Xử lý ảnh
│   │   ├── pdf_processor.py      # Xử lý file PDF
│   │   └── zip_processor.py      # Xử lý file ZIP
│   ├── utils/                    # Tiện ích
│   │   ├── sorting.py            # Sắp xếp tự nhiên
│   │   └── validators.py         # Kiểm tra dữ liệu
│   ├── templates/                # Jinja2 templates
│   │   ├── index.html            # Trang chủ
│   │   ├── details.html          # Chi tiết album
│   │   └── viewer.html           # Xem ảnh
│   └── static/                   # CSS, JS, assets
│
├── config/                       # Cấu hình ứng dụng
│   ├── base.py                   # Config cơ bản
│   ├── development.py            # Config dev
│   ├── production.py             # Config production
│   └── testing.py                # Config test
│
├── data/                         # Dữ liệu người dùng (gitignored)
│   ├── albums/                   # Albums đã mã hóa
│   ├── covers/                   # Ảnh bìa
│   ├── uploads/                  # File upload tạm
│   └── instance/                 # SQLite database
│
├── scripts/                      # Scripts tiện ích
├── docs/                         # Tài liệu
├── tests/                        # Unit tests
│
├── run.py                        # Entry point
├── init_db.py                    # Khởi tạo database
├── pyproject.toml                # Python dependencies
├── secret.key                    # Khóa mã hóa (tự động tạo)
└── .env.example                  # Mẫu biến môi trường
```

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python >= 3.12
- poppler-utils (cho PDF processing)

### Cài đặt

```bash
# Clone và vào thư mục
cd comic-album-manager

# Cài đặt dependencies (với uv)
uv sync

# Hoặc với pip
pip install -e .

# Cài poppler (cho xử lý PDF)
sudo apt install poppler-utils  # Ubuntu/Debian
brew install poppler            # macOS
```

### Chạy ứng dụng

```bash
# Development
python run.py

# Hoặc với Flask
flask run --host=0.0.0.0 --port=5000
```

Truy cập: http://localhost:5000

## 📦 Database Models

### ComicSeries
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(300) | Tên series |
| `cover_image` | String(300) | Ảnh bìa |
| `is_completed` | Boolean | Đã hoàn thành chưa |
| `albums` | Relationship | Danh sách album |

### ImageAlbum
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(300) | Tên album/chapter |
| `folder_path` | String(300) | Đường dẫn folder |
| `cover_image` | String(300) | Ảnh bìa |
| `series_id` | FK | Thuộc series nào |

### ImageFile
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `filename` | String | Tên file |
| `album_id` | FK | Thuộc album nào |

## 🔐 Bảo mật

- Tất cả ảnh được mã hóa với **Fernet (AES-128-CBC)**
- Key lưu trong `secret.key` (tự động tạo lần đầu)
- Ảnh chỉ giải mã khi serve cho client
- **⚠️ Quan trọng**: Backup `secret.key` - mất key = mất dữ liệu!

## 🛠️ API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Trang chủ |
| GET | `/album/<id>` | Chi tiết album |
| GET | `/viewer/<id>` | Xem ảnh album |
| POST | `/upload/folder` | Upload folder ảnh |
| POST | `/upload/pdf` | Upload file PDF |
| POST | `/upload/zip` | Upload file ZIP |
| GET | `/api/image/<album_id>/<filename>` | Lấy ảnh (decrypt) |
| GET | `/series/<id>` | Chi tiết series |
| POST | `/series/create` | Tạo series mới |

## 📝 Cấu hình

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Các biến môi trường:

| Biến | Mô tả | Mặc định |
|------|-------|----------|
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `DATABASE_URL` | Database connection | sqlite:///data/instance/database.db |
| `FLASK_ENV` | Môi trường | development |

## 🧪 Testing

```bash
# Chạy tests
pytest tests/

# Với coverage
pytest --cov=app tests/
```

## 📋 Workflow sử dụng

1. **Upload album**: Trang chủ → Upload (folder/PDF/ZIP)
2. **Tạo series**: Trang chủ → Tạo Series → Đặt tên
3. **Gán album vào series**: Chi tiết album → Chọn series
4. **Xem truyện**: Click album → Viewer

## 🔧 Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Database lỗi | Xóa `data/instance/database.db`, chạy lại |
| Import error | Chạy từ thư mục gốc project |
| PDF không convert | Cài `poppler-utils` |
| Ảnh không hiển thị | Kiểm tra `secret.key` còn nguyên |

## 📄 License

MIT License
