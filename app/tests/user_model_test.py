import time
import unittest

from faker import Faker

from app.models import Permission, Role
from config import Config
from app.factories import UserFactory, AnonymousUserFactory
from .. import create_app, db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # in memory database


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.faker = Faker("en_GB")
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = UserFactory.build()
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = UserFactory.build()
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        password1 = self.faker.password()
        password2 = self.faker.password()
        u = UserFactory.build(password=password1)
        self.assertTrue(u.verify_password(password1))
        self.assertFalse(u.verify_password(password2))

    def test_password_salts_are_random(self):
        password = self.faker.password()
        u1 = UserFactory.build(password=password)
        u2 = UserFactory.build(password=password)
        self.assertNotEqual(u1.password_hash, u2.password_hash)

    def test_valid_confirmation_token(self):
        u = UserFactory.build()
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = UserFactory.build()
        u2 = UserFactory.build()
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = UserFactory.build()
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_ping(self):
        u = UserFactory.build()
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)

    def test_gravatar(self):
        u = UserFactory.build(email="john@example.com")
        with self.app.test_request_context("/"):
            gravatar = u.gravatar()
            gravatar_256 = u.gravatar(size=256)
            gravatar_pg = u.gravatar(rating="pg")
            gravatar_retro = u.gravatar(default="retro")
        self.assertTrue("https://secure.gravatar.com/avatar/" + "d4c74594d841139328695756648b6bd6" in gravatar)
        self.assertTrue("s=256" in gravatar_256)
        self.assertTrue("r=pg" in gravatar_pg)
        self.assertTrue("d=retro" in gravatar_retro)

    def test_user_role(self):
        u = UserFactory.build()
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUserFactory.build()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
