import unittest

from faker import Faker

from config import Config
from kilc.models import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in memory database


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.fake = Faker('en_GB')

    def test_password_setter(self):
        u = User(password=self.fake.password())
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password=self.fake.password())
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        password1 = self.fake.password()
        password2 = self.fake.password()
        u = User(password=password1)
        self.assertTrue(u.verify_password(password1))
        self.assertFalse(u.verify_password(password2))

    def test_password_salts_are_random(self):
        password = self.fake.password()
        u1 = User(password=password)
        u2 = User(password=password)
        self.assertNotEqual(u1.password_hash, u2.password_hash)

    def test_avatar(self):
        u = User(name=self.fake.name(), email='john@example.com')
        self.assertEqual(u.avatar(128),
                         'https://www.gravatar.com/avatar/'
                         'd4c74594d841139328695756648b6bd6'
                         '?d=identicon&s=128')
