import unittest

from flask import current_app

from app import create_app
from app.models import user


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_user_model(self):
        user = User()
        user.username = "juli"
        user.email="cha"
        user.password = "reger"
        self.asserEqual(user.username,"juli")
        self.asserEqual(user.email,"cha")
        self.asserEqual(user.password,"reger")
if __name__ == '__main__':
    unittest.main()
