from random import randint

from sqlalchemy.exc import IntegrityError

from . import db
from .factories import UserFactory, PostFactory
from .models import User


def users(count=100):
    for i in range(count + 1):
        u = UserFactory.build()
        db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def posts(count=100):
    user_count = User.query.count()
    for i in range(user_count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = PostFactory(author=u)
        db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
