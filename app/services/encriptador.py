from cryptography.fernet import Fernet


class EncriptadorSV:
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key
    def encrypt_content(content,key):
        f = Fernet(key)
        content = f.encrypt(content.encode('utf-8'))
        return content
    @staticmethod
    def decrypt_content(content,key):
        content =Fernet(key).decrypt(content)
        content = content.decode('utf-8')
        return content