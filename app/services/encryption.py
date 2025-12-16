"""Encryption Service"""
import os
import io
from cryptography.fernet import Fernet

class EncryptionService:
    """Handles file encryption and decryption"""
    
    def __init__(self, key_file='secret.key'):
        self.key_file = key_file
        self.cipher = Fernet(self._load_key())
    
    def _load_key(self):
        """Load or generate encryption key"""
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        return open(self.key_file, 'rb').read()
    
    def save_encrypted(self, file_data, save_path):
        """Encrypt and save file data"""
        if isinstance(file_data, bytes):
            data = file_data
        else:
            # If it's a file object from form upload
            file_data.seek(0)
            data = file_data.read()
        
        encrypted_data = self.cipher.encrypt(data)
        with open(save_path, 'wb') as f:
            f.write(encrypted_data)
    
    def get_decrypted_file(self, file_path):
        """Read and decrypt file"""
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return io.BytesIO(decrypted_data)
