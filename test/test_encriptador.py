import unittest

from app import create_app, db
from app.models.encriptador import Encriptador


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

    def test_encriptador(self):
        encriptador = Encriptador()
        encriptador.content = "Texto de Prueba"
        self.assertEqual(encriptador.content, "Texto de Prueba")
        
    def test_encriptador_save(self):
        encriptador = Encriptador()
        encriptador.content="Texto de Prueba"
        encriptador.encrypt_content()
        encriptador.save()
        self.assertGreaterEqual(encriptador.id, 1)
        self.assertNotEqual(encriptador.content, "Texto de Prueba")
    
    def test_encriptador_delete(self):
        encriptador = Encriptador()
        encriptador.content="Texto de Prueba"
        encriptador.encrypt_content()
        encriptador.save()
        encriptador.delete()
        self.assertIsNone(Encriptador.query.get(encriptador.id))

    def test_encriptador_find(self):
        encriptador = Encriptador()
        encriptador.content="Texto de Prueba"
        encriptador.encrypt_content()
        encriptador.save()
        encriptador_find = encriptador.find(1)
        self.assertIsNotNone(encriptador_find)
        self.assertEqual(encriptador_find.id, encriptador.id)
        self.assertEqual(encriptador_find.content, encriptador.content)

    def test_encriptador_encrypt_content(self):
        encriptador = Encriptador()
        encriptador.content = "Texto de Prueba"
        encriptador.encrypt_content()
        print(encriptador.content)
        self.assertNotEqual(encriptador.content, "Texto de Prueba")
    def test_decrypt_content(self):
        encriptador = Encriptador()
        encriptador.content = "Texto de Prueba"
        encriptador.encrypt_content()
        encriptador.decrypt_content()
        encriptador.save()
        self.assertEqual(encriptador.content, 'Texto de Prueba')

if __name__ == "__main__":
    unittest.main()
