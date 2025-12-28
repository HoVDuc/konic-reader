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
│   │   ├── zip_processor.py      # Xử lý file ZIP
│   │   └── torrent_service.py    # Xử lý torrent (thử nghiệm)
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

### Routes chính
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Trang chủ (Thư viện) - hỗ trợ `?sort=name\|date&tag=tag_name&favorites=true` |
| GET | `/login` | Trang đăng nhập |
| POST | `/login` | Xác thực người dùng |
| GET | `/signup` | Trang đăng ký |
| POST | `/signup` | Đăng ký tài khoản mới |
| GET | `/logout` | Đăng xuất |

### Upload Routes (`/upload`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/upload/` | Trang Upload |
| POST | `/upload/folder` | Upload folder ảnh (hỗ trợ nhiều folder) |
| POST | `/upload/pdf` | Upload file PDF (xử lý nền) |
| POST | `/upload/zip` | Upload file ZIP (xử lý nền) |

### Album Routes (`/album`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/album/<id>` | Xem album trong reader |
| GET | `/album/details/<type>/<id>` | Trang chi tiết album/series |
| GET | `/album/image/<album_id>/<filename>` | Lấy ảnh (đã giải mã) |
| GET | `/album/cover/<filename>` | Lấy ảnh bìa |
| POST | `/album/rename/<type>/<id>` | Đổi tên album/series |
| POST | `/album/change_cover/<type>/<id>` | Đổi ảnh bìa |
| POST | `/album/set_cover_from_page/<album_id>/<filename>` | Đặt bìa từ trang trong album |
| POST | `/album/delete/<type>/<id>` | Xóa album/series |
| POST | `/album/add_to_series/<album_id>` | Thêm album vào series |
| POST | `/album/remove_from_series/<album_id>` | Xóa album khỏi series |
| POST | `/album/toggle_favorite/<type>/<id>` | Toggle yêu thích |
| POST | `/album/add_tag/<type>/<id>` | Thêm tag |
| POST | `/album/remove_tag/<type>/<id>` | Xóa tag |

### Series Routes (`/series`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/series/create` | Tạo series mới |
| POST | `/series/toggle/<id>` | Toggle trạng thái hoàn thành |

### Tags Routes (`/tags`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/tags/` | Trang quản lý Tags |
| POST | `/tags/edit/<id>` | Sửa tên tag |
| POST | `/tags/delete/<id>` | Xóa tag |

### API Routes (`/api`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/status/<task_id>` | Lấy trạng thái xử lý cho các tác vụ nền |

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
   - Folder: Chọn nhiều file ảnh hoặc nhiều folder cùng lúc
   - PDF: Sẽ được chuyển đổi thành ảnh (cần cài poppler-utils)
   - ZIP: Giải nén và mã hóa ảnh tự động
3. **Tạo series**: Vào trang Upload → Tạo Series → Đặt tên
4. **Gán album vào series**: Chi tiết album → Chọn series từ dropdown
   - Ảnh bìa của chapter đầu tiên sẽ tự động trở thành bìa series
5. **Quản lý Tags**: Vào trang Tags để sửa/xóa, hoặc thêm tag trực tiếp trong trang chi tiết
6. **Yêu thích**: Click icon ngôi sao để thêm vào danh sách yêu thích
7. **Xem truyện**: Click album → Viewer
   - Header tự ẩn khi cuộn xuống, hiện khi cuộn lên
   - Di chuyển giữa các chapter bằng nút prev/next
   - Nút Home để quay lại thư viện

## Tính năng chi tiết

### Trang thư viện
- Lọc theo tag hoặc yêu thích
- Sắp xếp theo tên hoặc ngày upload
- Xem series và album đơn lẻ

### Chi tiết Album
- Đổi tên album/series
- Thay đổi hoặc đặt ảnh bìa
- Thêm/xóa tags
- Bật/tắt yêu thích
- Gán vào series

### Xem ảnh (Viewer)
- Cuộn mượt qua các ảnh
- Header tự ẩn để đọc thoải mái
- Di chuyển giữa các chapter trong series

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
