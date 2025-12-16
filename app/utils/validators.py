"""File validation utilities"""

ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
ALLOWED_PDF_EXTENSIONS = {'.pdf'}
ALLOWED_ZIP_EXTENSIONS = {'.zip'}

def is_allowed_image(filename):
    """Check if filename has allowed image extension"""
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS

def is_allowed_pdf(filename):
    """Check if filename has allowed PDF extension"""
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_PDF_EXTENSIONS

def is_allowed_zip(filename):
    """Check if filename has allowed ZIP extension"""
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_ZIP_EXTENSIONS
