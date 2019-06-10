import factory

from .models import User, AnonymousUser, Post, Category, Tag


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    confirmed = True
    location = factory.Faker("city")
    about_me = factory.Faker("text")
    member_since = factory.Faker("past_date")


class AnonymousUserFactory(factory.Factory):
    class Meta:
        model = AnonymousUser


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Faker("word")


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = factory.Faker("word")


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("text")
