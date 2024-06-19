import os
import unittest

from flask import current_app

from app import create_app


class HomeResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)  # Crea un cliente de prueba
        self.base_url = os.getenv('API_BASE_URL')  # Obtén la URL base de la API desde una variable de entorno

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get(self.base_url)  # Realiza una petición GET a la URL base
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OK', response.data)
        

if __name__ == '__main__':
    unittest.main()