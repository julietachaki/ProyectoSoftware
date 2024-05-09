import unittest

from cryptography.fernet import Fernet
from flask import current_app

from app import create_app, db
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

    def test_text(self):
        text = Text()
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        self.assertEqual(text.content, "Hola mundo")
        self.assertEqual(text.length, 10)
        self.assertEqual(text.language, "es")

    def test_text_save(self):
        text = Text()
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        text.save()

        self.assertGreaterEqual(text.id, 1)
        self.assertEqual(text.content, "Hola mundo")
        self.assertEqual(text.length, 10)
        self.assertEqual(text.language, "es")

    def test_text_delete(self):
        text = Text()
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        text.save()
        text.delete()
        self.assertIsNone(Text.query.get(text.id))

    def test_text_find(self):
        text = Text()
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        text.save()
        text_find = Text.find(1)
        self.assertIsNotNone(text_find)
        self.assertEqual(text_find.id, text.id)
        self.assertEqual(text_find.content, text.content)

    def test_encrypt_content(self):
        text = Text()
        text.content = "Hola mundo"
        text.length = len(text.content)
        text.language = "es"
        text.save()

        key = Fernet.generate_key()

        text.encrypt_content(key)

        self.assertNotEqual(text.content, "Hola mundo")
        self.assertIsInstance(text.content, str)

    def test_change_content(self):
        # Crea un objeto Text y guarda una versión
        text = Text()
        text.content = "Hello world"
        text.length = len(text.content)
        text.language = "en"
        text.save()

        old_content = text.content

        # Cambia el contenido
        new_content = "Hola mundo"
        text.change_content(new_content)

        # Verifica que el contenido haya cambiado
        self.assertEqual(text.content, new_content)

        # Verifica que se haya guardado la versión anterior en TextHistory
        history = TextHistory.query.filter_by(text_id=text.id).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.content, old_content)


if __name__ == "__main__":
    unittest.main()