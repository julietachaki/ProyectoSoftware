import unittest

from cryptography.fernet import Fernet
from flask import current_app

from app import create_app, db
from app.models import User, UserData
from app.models.text import Text
from app.models.text_history import TextHistory


class TextTestCase(unittest.TestCase):
    def setUp(self):
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

    def create_text(self):
        text = Text()
        text.content = "Texto a Encriptar"
        text.length = len(text.content)
        text.language = "es"
        return text
    
    def test_text(self):
        text = self.create_text()
        self.assertEqual(text.content, "Texto a Encriptar")
        self.assertEqual(text.length, 17)
        self.assertEqual(text.language, "es")

    def test_text_save(self):
        text = self.create_text()
        text.save()
        self.assertGreaterEqual(text.id, 1)
        self.assertEqual(text.content, "Texto a Encriptar")
        self.assertEqual(text.length, 17)
        self.assertEqual(text.language, "es")
    
    def test_text_save_with_user(self):
        data = UserData()
        data.firstname = "Julieta"
        data.lastname = "Chaki"
        data.address = "Address 1234"
        data.city = "San Rafael"
        data.country = "Argentina"
        data.phone = "54260123456789"
        user = User(data)
        user.email = "test@test.com"
        user.username = "julietachaki"
        user.password = "Qvv3r7y"
        user.save()
        # Crea un texto y asigna el usuario
        text = self.create_text()
        text.user_id = user.id  # Asigna el usuario al texto
        text.save()
        # Verifica que el usuario asignado al texto sea el esperado
        self.assertEqual(text.user_id, user.id)

    def test_text_delete(self):
        text = self.create_text()
        text.save()
        text.delete()
        self.assertIsNone(Text.query.get(text.id))

    def test_text_find(self):
        text = self.create_text()
        text.save()
        text_find = Text.find(1)
        self.assertIsNotNone(text_find)
        self.assertEqual(text_find.id, text.id)
        self.assertEqual(text_find.content, text.content)


    def test_change_content(self):
        # Crea un objeto Text y guarda una versión
        text = self.create_text()
        text.save()
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

if __name__ == "__main__":
    unittest.main()