# Comic Album Manager

[**English**](README.md) | **Tiếng Việt**

Ứng dụng web Flask để quản lý và xem truyện tranh/album ảnh với tính năng mã hóa bảo mật.

## Tính năng chính

- **Upload đa dạng**: Hỗ trợ upload folder ảnh, file PDF, file ZIP
- **Mã hóa bảo mật**: Tất cả ảnh được mã hóa với Fernet (AES-128-CBC)
- **Quản lý Series**: Nhóm các album/chapter thành series
- **Tags & Favorites**: Gắn thẻ và đánh dấu yêu thích cho album/series
- **Viewer ảnh**: Xem ảnh với giao diện thân thiện, ẩn header khi cuộn
- **Xác thực người dùng**: Hệ thống đăng nhập với tính năng "Ghi nhớ đăng nhập"
- **Responsive**: Giao diện tương thích mobile

## Công nghệ sử dụng

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: SQLite
- **Mã hóa**: Fernet (thư viện cryptography)
- **Xử lý PDF**: pdf2image + poppler-utils
- **Frontend**: Jinja2 templates, CSS, JavaScript

## Cấu trúc dự án

```
comic-album-manager/
├── app/                          # Ứng dụng Flask chính
│   ├── __init__.py               # Application factory
│   ├── models/                   # Database models (SQLAlchemy)
│   │   ├── comic_series.py       # Model ComicSeries
│   │   ├── image_album.py        # Model ImageAlbum
│   │   ├── image_file.py         # Model ImageFile
│   │   ├── user.py               # Model User
│   │   └── tag.py                # Model Tag
│   ├── routes/                   # Route blueprints
│   │   ├── main.py               # Trang chủ
│   │   ├── auth.py               # Xác thực (đăng nhập/đăng ký/đăng xuất)
│   │   ├── upload.py             # Upload file/folder
│   │   ├── series.py             # Quản lý series
│   │   ├── album.py              # Quản lý album
│   │   ├── tags.py               # Quản lý tags
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
│   │   ├── login.html            # Trang đăng nhập
│   │   ├── signup.html           # Trang đăng ký
│   │   ├── upload.html           # Trang upload
│   │   ├── details.html          # Chi tiết album
│   │   ├── tags.html             # Quản lý tags
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

## Cài đặt & Chạy

### Yêu cầu
- Python >= 3.12
- poppler-utils (cho PDF processing)

### Cài đặt

```bash
# Clone và vào thư mục
git clone <repository-url>
cd comic-album-manager

# Cài đặt dependencies (với uv - khuyến nghị)
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

# Hoặc với Flask CLI
flask run --host=0.0.0.0 --port=5000
```

Truy cập: http://localhost:5000

## Database Models

### User
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `username` | String(80) | Tên đăng nhập (duy nhất) |
| `password_hash` | String(256) | Mật khẩu đã hash |

### ComicSeries
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(300) | Tên series |
| `cover_image` | String(300) | Ảnh bìa |
| `is_completed` | Boolean | Đã hoàn thành chưa |
| `is_favorite` | Boolean | Đánh dấu yêu thích |
| `albums` | Relationship | Danh sách album |
| `tags` | Relationship | Danh sách tags |

### ImageAlbum
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(300) | Tên album/chapter |
| `folder_path` | String(300) | Đường dẫn folder |
| `cover_image` | String(300) | Ảnh bìa |
| `series_id` | FK | Thuộc series nào |
| `is_favorite` | Boolean | Đánh dấu yêu thích |
| `tags` | Relationship | Danh sách tags |

### Tag
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(50) | Tên tag |

### ImageFile
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary key |
| `filename` | String | Tên file |
| `album_id` | FK | Thuộc album nào |

## Bảo mật

- Tất cả ảnh được mã hóa với **Fernet (AES-128-CBC)**
- Key lưu trong `secret.key` (tự động tạo lần đầu)
- Ảnh chỉ giải mã khi serve cho client
- Mật khẩu người dùng được hash trước khi lưu
- Tính năng "Ghi nhớ đăng nhập" sử dụng secure session cookies
- **⚠️ Quan trọng**: Backup `secret.key` - mất key = mất dữ liệu!

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Trang chủ (Thư viện) |
| GET | `/login` | Trang đăng nhập |
| POST | `/login` | Xác thực người dùng |
| GET | `/signup` | Trang đăng ký |
| POST | `/signup` | Đăng ký tài khoản mới |
| GET | `/logout` | Đăng xuất |
| GET | `/upload/` | Trang Upload |
| GET | `/tags/` | Quản lý Tags |
| GET | `/album/<id>` | Chi tiết album |
| GET | `/viewer/<id>` | Xem ảnh album |
| POST | `/upload/folder` | Upload folder ảnh |
| POST | `/upload/pdf` | Upload file PDF |
| POST | `/upload/zip` | Upload file ZIP |
| GET | `/api/image/<album_id>/<filename>` | Lấy ảnh (decrypt) |
| GET | `/series/<id>` | Chi tiết series |
| POST | `/series/create` | Tạo series mới |
| POST | `/album/toggle_favorite/<type>/<id>` | Toggle yêu thích |
| POST | `/album/add_tag/<type>/<id>` | Thêm tag |
| POST | `/album/remove_tag/<type>/<id>` | Xóa tag |

## Cấu hình

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

## Testing

```bash
# Chạy tests
pytest tests/

# Với coverage
pytest --cov=app tests/
```

## Workflow sử dụng

1. **Đăng ký/Đăng nhập**: Tạo tài khoản hoặc đăng nhập (tích "Ghi nhớ đăng nhập" để không cần đăng nhập lại)
2. **Upload album**: Vào trang Upload → Chọn loại (folder/PDF/ZIP)
3. **Tạo series**: Vào trang Upload → Tạo Series → Đặt tên
4. **Gán album vào series**: Chi tiết album → Chọn series
5. **Quản lý Tags**: Vào trang Tags để sửa/xóa, hoặc thêm tag trực tiếp trong trang chi tiết
6. **Yêu thích**: Click icon ngôi sao để thêm vào danh sách yêu thích
7. **Xem truyện**: Click album → Viewer (Header ẩn khi cuộn, nút Home để quay lại)

## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Database lỗi | Xóa `data/instance/database.db`, chạy lại |
| Import error | Chạy từ thư mục gốc project |
| PDF không convert | Cài `poppler-utils` |
| Ảnh không hiển thị | Kiểm tra `secret.key` còn nguyên |
| Lỗi đăng nhập | Xóa cookies trình duyệt, thử lại |

## License

MIT License
