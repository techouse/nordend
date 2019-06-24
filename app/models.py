from datetime import datetime
from hashlib import md5
from time import time

import bleach
import jwt
import pytz
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from slugify.slugify import slugify
from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login
from .bleach_settings import allowed_tags, allowed_styles, allowed_attributes


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
        return existing_role.id == id

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
        return cls.permissions.op("&")(Permission.FOLLOW) == Permission.FOLLOW

    @hybrid_property
    def comment(self):
        return self.has_permission(Permission.COMMENT)

    @comment.expression
    def comment(cls):
        return cls.permissions.op("&")(Permission.COMMENT) == Permission.COMMENT

    @hybrid_property
    def write(self):
        return self.has_permission(Permission.WRITE)

    @write.expression
    def write(cls):
        return cls.permissions.op("&")(Permission.WRITE) == Permission.WRITE

    @hybrid_property
    def moderate(self):
        return self.has_permission(Permission.MODERATE)

    @moderate.expression
    def moderate(cls):
        return cls.permissions.op("&")(Permission.MODERATE) == Permission.MODERATE

    @hybrid_property
    def admin(self):
        return self.has_permission(Permission.ADMIN)

    @admin.expression
    def admin(cls):
        return cls.permissions.op("&")(Permission.ADMIN) == Permission.ADMIN

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
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    posts = db.relationship("PostAuthor", lazy="dynamic")

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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def generate_confirmation_send_again_token(self, expires_in=600):
        return jwt.encode(
            {"send_again": self.id, "exp": time() + expires_in}, current_app.config["SECRET_KEY"], algorithm="HS256"
        ).decode("utf-8")

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

    @staticmethod
    def confirm(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        user = User.query.get(data["confirm"])
        if not user:
            return False
        user.confirmed = True
        user.update()
        return True

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_confirmation_send_again_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])["send_again"]
        except:
            return
        return User.query.get(id)

    @classmethod
    def is_unique(cls, id, email):
        existing_user = cls.query.filter_by(email=email).first()
        if existing_user is None:
            return True
        return existing_user.id == id

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
    posts = db.relationship("PostCategory", lazy="dynamic")

    @staticmethod
    def on_changed_name(target, value, oldvalue, initiator):
        target.slug = slugify(value)

    @classmethod
    def is_unique(cls, id, name):
        existing_category = cls.query.filter_by(name=name).first()
        if existing_category is None:
            return True
        return existing_category.id == id

    def __repr__(self):
        return "<Category {}>".format(self.name)


db.event.listen(Category.name, "set", Category.on_changed_name)


class PostTag(db.Model, AddUpdateDelete):
    __tablename__ = "post_tags"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    post = db.relationship("Post", backref=db.backref("post_tags", cascade="all, delete-orphan", lazy="dynamic"))
    tag = db.relationship("Tag", backref=db.backref("post_tags", cascade="all, delete-orphan", lazy="dynamic"))

    def __repr__(self):
        return "<PostTag {}, {}>".format(self.post.title, self.tag.name)


class PostImage(db.Model, AddUpdateDelete):
    __tablename__ = "post_images"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), primary_key=True)
    primary = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    post = db.relationship("Post", backref=db.backref("post_images", cascade="all, delete-orphan", lazy="dynamic"))
    image = db.relationship("Image", backref=db.backref("post_images", cascade="all, delete-orphan", lazy="dynamic"))

    def __repr__(self):
        return "<PostImage {}, {}>".format(self.post.title, self.image.original_filename)


class PostAuthor(db.Model, AddUpdateDelete):
    __tablename__ = "post_authors"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    primary = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    post = db.relationship("Post", backref=db.backref("post_authors", cascade="all, delete-orphan", lazy="dynamic"))
    user = db.relationship("User", backref=db.backref("post_authors", cascade="all, delete-orphan", lazy="dynamic"))

    def __repr__(self):
        return "<PostAuthor {}, {}>".format(self.post.title, self.user.name)


class PostCategory(db.Model, AddUpdateDelete):
    __tablename__ = "post_categories"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), primary_key=True)
    primary = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    post = db.relationship("Post", backref=db.backref("post_categories", cascade="all, delete-orphan", lazy="dynamic"))
    category = db.relationship(
        "Category", backref=db.backref("post_categories", cascade="all, delete-orphan", lazy="dynamic")
    )

    def __repr__(self):
        return "<PostCategory {}, {}>".format(self.post.title, self.category.name)


related_posts = db.Table(
    "related_posts",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("related_post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("created_at", db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False),
)


class Post(db.Model, AddUpdateDelete):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    sub_title = db.Column(db.String(1024), index=True)
    slug = db.Column(db.String(255), index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    is_draft = db.Column(db.Boolean, default=True, index=True, nullable=False)
    is_published = db.Column(db.Boolean, default=False, index=True, nullable=False)
    published_at = db.Column(db.DateTime, index=True, nullable=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP, index=True, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )
    # relationships
    authors = db.relationship("PostAuthor", lazy="dynamic")
    categories = db.relationship("PostCategory", lazy="dynamic")
    images = db.relationship("PostImage", lazy="dynamic")
    _tags = db.relationship("PostTag", lazy="dynamic")
    _related = db.relationship(
        "Post",
        secondary=related_posts,
        primaryjoin=id == related_posts.c.post_id,
        secondaryjoin=id == related_posts.c.related_post_id,
        backref=db.backref("related_posts", lazy="dynamic"),
        lazy="dynamic",
    )

    @classmethod
    def is_unique(cls, id, category, slug):
        if not category:
            return True
        existing_post = cls.query.filter_by(slug=slug).filter(PostCategory.category_id == category.id).first()
        if existing_post is None:
            return True
        return existing_post.id == id

    @staticmethod
    def on_changed_title(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = bleach.linkify(
            bleach.clean(
                value,
                tags=allowed_tags,
                styles=allowed_styles,
                attributes=allowed_attributes,
                strip=True,
                strip_comments=True,
            )
        )

    @hybrid_property
    def author(self):
        author = self.authors.filter(PostAuthor.primary.is_(True)).first()
        return author.user if author else None

    @author.setter
    def author(self, value):
        if isinstance(value, User):
            value = value.id
        current_author = self.authors.filter(PostAuthor.primary.is_(True)).first()
        new_author = self.authors.filter(PostAuthor.user_id == value).first()
        if current_author:
            if current_author.user_id == value:
                return
            current_author.primary = False
        if new_author:
            new_author.primary = True
        else:
            self.authors.append(PostAuthor(user_id=value, primary=True))

    @hybrid_property
    def category(self):
        category = self.categories.filter(PostCategory.primary.is_(True)).first()
        return category.category if category else None

    @category.setter
    def category(self, value):
        if isinstance(value, Category):
            value = value.id
        current_category = self.categories.filter(PostCategory.primary.is_(True)).first()
        new_category = self.categories.filter(PostCategory.category_id == value).first()
        if current_category:
            if current_category.category_id == value:
                return
            current_category.primary = False
        if new_category:
            new_category.primary = True
        else:
            self.categories.append(PostCategory(category_id=value, primary=True))

    @hybrid_property
    def additional_categories(self):
        return self.categories.filter(PostCategory.primary.isnot(True))

    @additional_categories.setter
    def additional_categories(self, categories):
        ids = set()
        for category in categories:
            if isinstance(category, Category):
                ids.add(category.id)
            else:
                ids.add(category)
        current = set(
            category[0] for category in self.categories.filter(PostCategory.primary.isnot(True)).values("category_id")
        )
        ids_to_delete = current - ids
        if ids_to_delete:
            self.categories.filter(PostCategory.primary.isnot(True)).filter(
                PostCategory.category_id.in_(list(ids_to_delete))
            ).delete(synchronize_session="fetch")
        ids_to_append = ids - current
        if ids_to_append:
            for category_id in ids_to_append:
                self.categories.append(PostCategory(category_id=category_id, primary=False))

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        ids = set()
        for tag in tags:
            if isinstance(tag, Tag):
                ids.add(tag.id)
            else:
                ids.add(tag)
        current = set(tag[0] for tag in self._tags.values("tag_id"))
        ids_to_delete = current - ids
        if ids_to_delete:
            self._tags.filter(PostTag.tag_id.in_(list(ids_to_delete))).delete(synchronize_session="fetch")
        ids_to_append = ids - current
        if ids_to_append:
            for tag_id in ids_to_append:
                self._tags.append(PostTag(tag_id=tag_id))

    @hybrid_property
    def related(self):
        return self._related

    @related.setter
    def related(self, related):
        ids = set()
        for related_post in related:
            if isinstance(related_post, Post):
                ids.add(related_post.id)
            else:
                ids.add(related_post)
        current = set(related_post[0] for related_post in self._related.values("related_post_id"))
        ids_to_delete = current - ids
        if ids_to_delete:
            for related_post_id in ids_to_delete:
                self._related.remove(Post.query.get(related_post_id))
        ids_to_append = ids - current
        if ids_to_append:
            for related_post_id in ids_to_append:
                self._related.append(Post.query.get(related_post_id))

    @hybrid_property
    def image(self):
        image = self.images.filter(PostImage.primary.is_(True)).first()
        return image.image if image else None

    @image.setter
    def image(self, value):
        if isinstance(value, Image):
            value = value.id
        current_image = self.images.filter(PostImage.primary.is_(True)).first()
        new_image = self.images.filter(PostImage.image_id == value).first()
        if current_image:
            if current_image.image_id == value:
                return
            current_image.primary = False
        if new_image:
            new_image.primary = True
        else:
            self.images.append(PostImage(image_id=value, primary=True))

    @hybrid_property
    def published(self):
        return (
            self.is_draft is False
            and self.is_published is True
            and self.published_at is not None
            and self.published_at.astimezone(pytz.utc) <= datetime.now(pytz.utc)
        )

    @published.expression
    def published(cls):
        return and_(
            cls.is_draft.is_(False), cls.is_published.is_(True), cls.published_at <= db.func.current_timestamp()
        )

    @published.setter
    def published(self, date_time):
        self.is_draft = False
        self.is_published = True
        self.published_at = date_time

    @hybrid_property
    def draft(self):
        return self.is_draft is True and self.is_published is False

    @draft.expression
    def draft(cls):
        return and_(cls.is_draft.is_(True), cls.is_published.is_(False))

    @draft.setter
    def draft(self, value):
        self.is_draft = value
        self.is_published = not value
        if value:
            self.published_at = None

    def __repr__(self):
        return "<Post {}>".format(self.title)


db.event.listen(Post.title, "set", Post.on_changed_title)
db.event.listen(Post.body, "set", Post.on_changed_body)


class ImageTag(db.Model, AddUpdateDelete):
    __tablename__ = "image_tags"
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    image = db.relationship("Image", backref=db.backref("image_tags", cascade="all, delete-orphan", lazy="dynamic"))
    tag = db.relationship("Tag", backref=db.backref("image_tags", cascade="all, delete-orphan", lazy="dynamic"))

    def __repr__(self):
        return "<ImageTag {}, {}>".format(self.image.original_filename, self.tag.name)


class Image(db.Model, AddUpdateDelete):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    hash = db.Column(db.CHAR(64), index=True, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    original_filename = db.Column(db.String(255))
    width = db.Column(db.BigInteger, default=0)
    height = db.Column(db.BigInteger, default=0)
    sizes = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.TIMESTAMP, index=True, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP, index=True, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )
    # relationships
    _tags = db.relationship("ImageTag", lazy="dynamic")
    posts = db.relationship("PostImage", lazy="dynamic")

    @hybrid_property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        ids = set()
        for tag in tags:
            if isinstance(tag, Tag):
                ids.add(tag.id)
            else:
                ids.add(tag)
        current = set(tag[0] for tag in self._tags.values("tag_id"))
        ids_to_delete = current - ids
        if ids_to_delete:
            self._tags.filter(ImageTag.tag_id.in_(list(ids_to_delete))).delete(synchronize_session="fetch")
        ids_to_append = ids - current
        if ids_to_append:
            for tag_id in ids_to_append:
                self._tags.append(ImageTag(tag_id=tag_id))


class Tag(db.Model, AddUpdateDelete):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    posts = db.relationship("PostTag", lazy="dynamic")
    images = db.relationship("ImageTag", lazy="dynamic")

    @staticmethod
    def on_changed_name(target, value, oldvalue, initiator):
        target.slug = slugify(value)

    @classmethod
    def is_unique(cls, id, name):
        existing_tag = cls.query.filter_by(name=name).first()
        if existing_tag is None:
            return True
        return existing_tag.id == id

    def __repr__(self):
        return "<Tag {}>".format(self.name)


db.event.listen(Tag.name, "set", Tag.on_changed_name)
