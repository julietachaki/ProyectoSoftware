import base64
import hashlib

from cryptography.fernet import Fernet


class EncriptadorSV:
    def generate_key(self,key):
        new_key = hashlib.sha256(key.encode()).digest()
        # Encode the key in base64 to make it valid for Fernet
        return base64.urlsafe_b64encode(new_key)
    
    def encrypt_content(self,content, key):
        f = Fernet(key)
        encrypted_content = f.encrypt(content.encode('utf-8'))
        content = encrypted_content.decode('utf-8')
        return content

    def decrypt_content(self,content, key):
        f = Fernet(key)
        decrypted_content = f.decrypt(content.encode('utf-8'))
        return decrypted_content.decode('utf-8')