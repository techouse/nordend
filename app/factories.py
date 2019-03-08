import factory
from .models import User, AnonymousUser


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    username = factory.Faker("word")
    password = factory.Faker("password")


class AnonymousUserFactory(factory.Factory):
    class Meta:
        model = AnonymousUser
