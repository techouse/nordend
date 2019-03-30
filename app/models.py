from datetime import datetime
from hashlib import md5
from time import time

import bleach
import jwt
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from slugify.slugify import slugify
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


class AddUpdateDelete:
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model, AddUpdateDelete):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @classmethod
    def is_unique(cls, id, name):
        existing_role = cls.query.filter_by(name=name).first()
        if existing_role is None:
            return True
        else:
            if existing_role.id == id:
                return True
            else:
                return False

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            "Moderator": [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            "Administrator": [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,
                Permission.ADMIN,
            ],
        }
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()

    @hybrid_property
    def follow(self):
        return self.has_permission(Permission.FOLLOW)

    @follow.expression
    def follow(cls):
        return cls.permissions >= Permission.FOLLOW

    @hybrid_property
    def comment(self):
        return self.has_permission(Permission.COMMENT)

    @comment.expression
    def comment(cls):
        return cls.permissions >= Permission.COMMENT

    @hybrid_property
    def write(self):
        return self.has_permission(Permission.WRITE)

    @write.expression
    def write(cls):
        return cls.permissions >= Permission.WRITE

    @hybrid_property
    def moderate(self):
        return self.has_permission(Permission.MODERATE)

    @moderate.expression
    def moderate(cls):
        return cls.permissions >= Permission.MODERATE

    @hybrid_property
    def admin(self):
        return self.has_permission(Permission.ADMIN)

    @admin.expression
    def admin(cls):
        return cls.permissions >= Permission.ADMIN

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(UserMixin, db.Model, AddUpdateDelete):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), nullable=False, index=True)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=db.func.current_timestamp())
    last_seen = db.Column(db.DateTime, default=db.func.current_timestamp())
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship("Post", backref="author", lazy="dynamic", passive_deletes=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in set(current_app.config["ADMINS"]):
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    def generate_confirmation_token(self, expires=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expires)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["id"])

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

    @classmethod
    def is_unique(cls, id, email):
        existing_user = cls.query.filter_by(name=email).first()
        if existing_user is None:
            return True
        else:
            if existing_user.id == id:
                return True
            else:
                return False

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar_hash(self):
        return md5(self.email.lower().encode("utf-8")).hexdigest()

    def gravatar(self, size=100, default="identicon", rating="g"):
        url = "https://secure.gravatar.com/avatar"
        hash = self.avatar_hash or self.gravatar_hash()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return "<User {}>".format(self.name)


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model, AddUpdateDelete):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    posts = db.relationship("Post", backref="category", lazy=True, passive_deletes=True)

    @staticmethod
    def on_changed_name(target, value, oldvalue, initiator):
        target.slug = slugify(value)

    @classmethod
    def is_unique(cls, id, name):
        existing_category = cls.query.filter_by(name=name).first()
        if existing_category is None:
            return True
        else:
            if existing_category.id == id:
                return True
            else:
                return False

    def __repr__(self):
        return "<Category {}>".format(self.name)


db.event.listen(Category.name, "set", Category.on_changed_name)


class Post(db.Model, AddUpdateDelete):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    slug = db.Column(db.String(255), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp())

    @classmethod
    def is_unique(cls, id, category, slug):
        existing_post = cls.query.filter_by(category_id=category.id, slug=slug).first()
        if existing_post is None:
            return True
        else:
            if existing_post.id == id:
                return True
            else:
                return False

    @staticmethod
    def on_changed_title(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "pre",
            "strong",
            "ul",
            "h1",
            "h2",
            "h3",
            "p",
        ]
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format="html"), tags=allowed_tags, strip=True)
        )

    def __repr__(self):
        return "<Post {}>".format(self.title)


db.event.listen(Post.title, "set", Post.on_changed_title)
db.event.listen(Post.body, "set", Post.on_changed_body)
