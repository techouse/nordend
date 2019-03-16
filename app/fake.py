from random import randint

from sqlalchemy.exc import IntegrityError

from . import db
from .factories import UserFactory, PostFactory, CategoryFactory
from .models import User, Category, Role


def roles():
    Role.insert_roles()


def users(count=100):
    for i in range(count + 1):
        r = Role.query.first()
        u = UserFactory.build(role=r)
        db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def categories(count=10):
    for i in range(count + 1):
        c = CategoryFactory.build()
        db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def posts(count=100):
    user_count = User.query.count()
    category_count = Category.query.count()
    for i in range(user_count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        c = Category.query.offset(randint(0, category_count - 1)).first()
        p = PostFactory(author=u, category=c)
        db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
