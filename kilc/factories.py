import factory
from .models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")
