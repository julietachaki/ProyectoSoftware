import unittest

from cryptography.fernet import Fernet
from flask import current_app

from app import create_app, db
from app.models.encriptador import Encriptador
from app.models.text import Text


class EncriptadorTestCase(unittest.TestCase):
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

    
if __name__ == "__main__":
    unittest.main()