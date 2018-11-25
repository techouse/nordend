import unittest

from faker import Faker

from kilc import app, db
from kilc.models import User

fake = Faker('sl_SI')


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # in memory database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(name=fake.name())
        password = fake.password()
        u.set_password(password)
        self.assertFalse(u.check_password(fake.password()))
        self.assertTrue(u.check_password(password))

    def test_avatar(self):
        u = User(name=fake.name(), email='john@example.com')
        self.assertEqual(u.avatar(128),
                         'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128')


if __name__ == '__main__':
    unittest.main(verbosity=2)
