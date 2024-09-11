import unittest

from cryptography.fernet import Fernet
from flask import current_app

from app import create_app, db
from app.models import User, UserData
from app.models.text import Text
from app.models.text_history import TextHistory
from app.services.encriptador import EncriptadorSV
from app.services.text_services import TextService
from app.services.user_services import UserService

user_service = UserService()
text_service= TextService()
encriptador = EncriptadorSV()

class TextTestCase(unittest.TestCase):
    def setUp(self):
        self.USERNAME_PRUEBA = 'julichaki'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = '123456'
        self.ADDRESS_PRUEBA = 'Address 1234'
        self.FIRSTNAME_PRUEBA = 'Juli'
        self.LASTNAME_PRUEBA = 'Chaki'
        self.PHONE_PRUEBA = '54260123456789'
        self.CITY_PRUEBA = 'San Rafael'
        self.COUNTRY_PRUEBA = 'Argentina'
        self.CONTENT = "Texto a Encriptar"
        self.LENGHT = len(self.CONTENT)
        self.LANGUAJE = "es"

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def check(self, text):
        self.assertEqual(text.content, self.CONTENT)
        self.assertEqual(text.length, self.LENGHT)
        self.assertEqual(text.language, self.LANGUAJE)
    
    def test_text(self):
        text = self.__get_text()
        self.assertEqual(text.content, self.CONTENT)
        self.assertEqual(text.length, self.LENGHT)
        self.assertEqual(text.language, self.LANGUAJE)

    def test_text_save(self):
        text = self.__get_text()
        text_service.save(text)
        self.assertGreaterEqual(text.id, 1)
        self.check(text)


    
    def test_text_save_with_user(self):
        user = self.__get_user()
        user_service.save(user)
        # Crea un texto y asigna el usuario
        text = self.__get_text()
        text.user_id = user.id  # Asigna el usuario al texto
        text_service.save(text)
        # Verifica que el usuario asignado al texto sea el esperado
        self.check(text)
        self.assertEqual(text.user_id, user.id)

    def test_text_encrypt(self):
        text = self.__get_text()
        text_service.save(text)
        key=encriptador.generate_key("123")
        text.content=  encriptador.encrypt_content(text.content,key)
        text_service.update(text, text.id)
        print(text.content)
        self.assertNotEqual(text.content, self.CONTENT)


    def test_text_desencrypt(self):
        text = self.__get_text()
        text_service.save(text)
        key =encriptador.generate_key("123")
        text.content=  encriptador.encrypt_content(text.content,key)
        text_service.update(text, text.id)
        text.content = encriptador.decrypt_content(text.content , key)
        text_service.update(text, text.id)
        print(text.content)
        self.assertEqual(text.content, self.CONTENT)

    def test_text_delete(self):
        text = self.__get_text()
        text_service.save(text)
        text_service.delete(text)
        self.assertIsNone(Text.query.get(text.id))

    def test_text_find(self):
        text = self.__get_text()
        text_service.save(text)
        text_find = text_service.find(1)
        self.assertIsNotNone(text_find)
        self.assertEqual(text_find.id, text.id)
        self.assertEqual(text_find.content, text.content)


    def test_change_content(self):
        # Crea un objeto Text y guarda una versión
        text = self.__get_text()
        text_service.save(text)
        old_content = text.content
        # Cambia el contenido
        new_content = "Texto a Nuevo  Encriptar"
        text.change_content(new_content)
        # Verifica que el contenido haya cambiado
        self.assertEqual(text.content, new_content)
        # Verifica que se haya guardado la versión anterior en TextHistory
        history = TextHistory.query.filter_by(text_id=text.id).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.content, old_content)
        
    def __get_text(self):
        text = Text()
        text.content = self.CONTENT
        text.length = self.LENGHT
        text.language = self.LANGUAJE
        return text
    def __get_user(self):
        data = UserData()
        data.firstname = self.FIRSTNAME_PRUEBA
        data.lastname = self.LASTNAME_PRUEBA
        data.phone = self.PHONE_PRUEBA
        data.address = self.ADDRESS_PRUEBA
        data.city = self.CITY_PRUEBA
        data.country = self.COUNTRY_PRUEBA
        
        user = User(data)
        user.username = self.USERNAME_PRUEBA
        user.email = self.EMAIL_PRUEBA
        user.password = self.PASSWORD_PRUEBA
        return user

if __name__ == "__main__":
    unittest.main()