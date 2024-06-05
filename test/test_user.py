import unittest

from flask import current_app

from app import create_app, db
from app.models import User, UserData


class UserTestCase(unittest.TestCase):
    """
    Test User model
    Necesitamos aplicar principios como DRY (Don't Repeat Yourself) y KISS (Keep It Simple, Stupid).
    YAGNI (You Aren't Gonna Need It) y SOLID (Single Responsibility Principle).
    """

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def create_user(self):
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
        return user

    def check_data(self, user):
        self.assertTrue(user.email, "test@test.com")
        self.assertTrue(user.username, "julietachaki")
        self.assertTrue(user.password, "Qvv3r7y")
        self.assertIsNotNone(user.data)
        self.assertTrue(user.data.address, "Address 1234")
        self.assertTrue(user.data.firstname, "Julieta")
        self.assertTrue(user.data.lastname, "Chaki")
        self.assertTrue(user.data.phone, "54260123456789")

    def test_user(self):
        user = self.create_user()
        self.check_data(user)

    def test_user_save(self):
        user = self.create_user()
        user.save()
        self.assertGreaterEqual(user.id, 1)
        self.check_data(user)

    def test_user_delete(self):
        user = self.create_user()
        user.save()
        user.delete()
        self.assertIsNone(User.find(user.id))

    def test_user_all(self):
        user = self.create_user()
        user.save()
        users = User.all()
        self.assertGreaterEqual(len(users), 1)

    def test_user_find(self):
        user = self.create_user()
        user.save()
        user_find = User.find(1)
        self.assertIsNotNone(user_find)
        self.assertEqual(user_find.id, user.id)
        self.assertEqual(user_find.email, user.email)

if __name__ == "__main__":
    unittest.main()