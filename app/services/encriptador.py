import base64
import hashlib

from cryptography.fernet import Fernet


class EncriptadorSV:
    @staticmethod
    def generate_key(key):
        new_key = hashlib.sha256(key.encode()).digest()
        # Encode the key in base64 to make it valid for Fernet
        return base64.urlsafe_b64encode(new_key)
    
    @staticmethod
    def encrypt_content(content, key):
        f = Fernet(key)
        encrypted_content = f.encrypt(content.encode('utf-8'))
        return encrypted_content.decode('utf-8')
    
    @staticmethod
    def decrypt_content(content, key):
        f = Fernet(key)
        decrypted_content = f.decrypt(content.encode('utf-8'))
        return decrypted_content.decode('utf-8')