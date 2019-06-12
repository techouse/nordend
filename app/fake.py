from random import randint

from sqlalchemy.exc import IntegrityError

from . import db
from .factories import UserFactory, PostFactory, CategoryFactory, TagFactory
from .models import User, Category, Role, Tag, PostCategory, PostAuthor, PostTag


def roles():
    Role.insert_roles()


def users(count=24):
    for i in range(count + 1):
        role = Role.query.first()
        user = UserFactory.build(role=role)
        db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def categories(count=12):
    for i in range(count + 1):
        category = CategoryFactory.build()
        db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def tags(count=24):
    for i in range(count + 1):
        tag = TagFactory.build()
        db.session.add(tag)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def posts(count=100):
    user_count = User.query.count()
    category_count = Category.query.count()
    tag_count = Tag.query.count()
    for i in range(user_count):
        user = User.query.offset(randint(0, user_count - 1)).first()
        tag = Tag.query.offset(randint(0, tag_count - 1)).first()
        category = Category.query.offset(randint(0, category_count - 1)).first()
        post = PostFactory()
        post.tags.append(PostTag(tag=tag))
        post.authors.append(PostAuthor(user=user, primary=True))
        post.categories.append(PostCategory(category=category, primary=True))
        db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
