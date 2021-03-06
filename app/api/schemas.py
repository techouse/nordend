from datetime import datetime
from urllib.parse import quote_plus

import pytz
import simplejson as json
from flask import current_app
from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_load, validates_schema, ValidationError
from marshmallow import validate

from app import redis
from .broadcast.post import PostBroadcast
from .validators import valid_permission, valid_password_reset_token
from ..models import Post, User, Role, Category, Image, Tag, PostCategory, PostAuthor, PostImage, PostTag, ImageTag
from ..redis_keys import locked_posts_redis_key

ma = Marshmallow()


class ResetPasswordRequestSchema(ma.Schema):
    email = fields.Email(required=True, load_only=True, validate=validate.Email())


class ResetPasswordTokenSchema(ma.Schema):
    token = fields.String(required=True, load_only=True, validate=valid_password_reset_token)


class ResetPasswordSchema(ma.Schema):
    token = fields.String(required=True, load_only=True, validate=valid_password_reset_token)
    password = fields.String(required=True, load_only=True, validate=lambda x: 8 <= len(x) <= 128)
    password_repeat = fields.String(required=True, load_only=True, validate=lambda x: 8 <= len(x) <= 128)

    @validates_schema
    def validate_passwords(self, data):
        if data["password"] != data["password_repeat"]:
            raise ValidationError("The password confirmation does not match the password", "password_repeat")


class RegistrationSchema(ma.Schema):
    name = fields.String(required=True, load_only=True, validate=lambda x: 3 <= len(x) <= 255)
    email = fields.Email(required=True, load_only=True, validate=validate.Email())
    password = fields.String(required=True, load_only=True, validate=lambda x: 8 <= len(x) <= 128)
    password_repeat = fields.String(required=True, load_only=True, validate=lambda x: 8 <= len(x) <= 128)

    @validates_schema
    def validate_passwords(self, data):
        if data["password"] != data["password_repeat"]:
            raise ValidationError("The password confirmation does not match the password", "password_repeat")


class RegistrationConfirmationSchema(ma.Schema):
    token = fields.String(required=True, load_only=True)


class RoleSchema(ma.Schema):
    class Meta:
        model = Role

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=lambda x: 0 < len(x) <= 64)
    default = fields.Boolean(required=True)
    follow = fields.Boolean(dump_only=True)
    comment = fields.Boolean(dump_only=True)
    write = fields.Boolean(dump_only=True)
    moderate = fields.Boolean(dump_only=True)
    admin = fields.Boolean(dump_only=True)
    permissions = fields.Integer(load_only=True, validate=valid_permission)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.role", id="<id>", _external=True),
            "collection": ma.URLFor("api.roles", _external=True),
            "relationships": {"users": ma.URLFor("api.role_users", id="<id>", _external=True)},
        }
    )


class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(load_only=True, validate=lambda x: 8 <= len(x) <= 128)
    otp_enabled = fields.Bool(dump_only=True)
    confirmed = fields.Boolean(required=True)
    name = fields.String(required=True, validate=lambda x: 3 <= len(x) <= 255)
    location = fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255)
    about_me = fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 2 ** 16)
    member_since = fields.DateTime(dump_only=True, format="iso8601")
    last_seen = fields.DateTime(dump_only=True, format="iso8601")
    created_at = fields.DateTime(dump_only=True, format="iso8601")
    updated_at = fields.DateTime(dump_only=True, format="iso8601")
    role = fields.Nested("RoleSchema", exclude=("users",))
    role_id = fields.Integer(required=True, validate=lambda x: x > 0 and Role.query.get(x) is not None)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.user", id="<id>", _external=True),
            "collection": ma.URLFor("api.users", _external=True),
            "relationships": {"posts": ma.URLFor("api.user_posts", id="<id>", _external=True)},
        }
    )


class CategorySchema(ma.Schema):
    class Meta:
        model = Category

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=lambda x: 0 < len(x) <= 255)
    slug = fields.String(dump_only=True)
    posts = fields.Nested("PostCategorySchema", many=True, exclude=("category",))
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.category", id="<id>", _external=True),
            "collection": ma.URLFor("api.categories", _external=True),
            "relationships": {"posts": ma.URLFor("api.category_posts", id="<id>", _external=True)},
        }
    )


class PostAuthorSchema(ma.Schema):
    class Meta:
        model = PostAuthor

    user = fields.Nested("UserSchema", only=("id", "name", "email", "links"))
    post = fields.Nested("PostSchema", only=("id", "title", "slug", "links"))
    primary = fields.Boolean()


class PostCategorySchema(ma.Schema):
    class Meta:
        model = PostCategory

    category = fields.Nested("CategorySchema", only=("id", "name", "slug", "links"))
    post = fields.Nested("PostSchema", only=("id", "title", "slug", "links"))
    primary = fields.Boolean()


class PostImageSchema(ma.Schema):
    class Meta:
        model = PostImage

    image = fields.Nested("ImageSchema", only=("id", "title", "public_path", "sizes", "original_filename", "links"))
    post = fields.Nested("PostSchema", only=("id", "title", "slug", "links"))
    primary = fields.Boolean()


class PostTagSchema(ma.Schema):
    class Meta:
        model = PostTag

    tag = fields.Nested("TagSchema", only=("id", "name", "slug"))
    post = fields.Nested("PostSchema", only=("id", "title", "slug", "links"))


class PostSchema(ma.Schema):
    class Meta:
        model = Post

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=lambda x: 0 < len(x) <= 255)
    sub_title = fields.String(allow_none=True)
    slug = fields.String(dump_only=True)
    body = fields.String(required=True, validate=lambda x: 0 <= len(x) <= 2 ** 16)
    body_html = fields.String(dump_only=True)
    draft = fields.Boolean()
    published = fields.Boolean()
    published_at = fields.DateTime(allow_none=True, format="iso8601")
    created_at = fields.DateTime(dump_only=True, format="iso8601")
    updated_at = fields.DateTime(dump_only=True, format="iso8601")
    author = fields.Nested("UserSchema", only=("id", "name", "email", "links"), dump_only=True)
    authors = fields.Nested("PostAuthorSchema", many=True, exclude=("post",))
    category = fields.Nested("CategorySchema", only=("id", "name", "slug", "links"), dump_only=True)
    additional_categories = fields.Nested("PostCategorySchema", many=True, exclude=("post",))
    image = fields.Nested(
        "ImageSchema", only=("id", "title", "public_path", "sizes", "original_filename", "links"), dump_only=True
    )
    images = fields.Nested("PostImageSchema", many=True, exclude=("post",))
    tags = fields.Nested("PostTagSchema", many=True, only=("tag",))
    related = fields.Nested("PostSchema", many=True, only=("id", "title", "slug", "links"))
    locked = fields.Method("is_locked", dump_only=True)
    locked_since = fields.Method("get_locked_since", dump_only=True)
    lock_expires = fields.Method("get_lock_expires", dump_only=True)
    locked_by = fields.Method("get_locked_by", dump_only=True)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.post", id="<id>", _external=True),
            "collection": ma.URLFor("api.posts", _external=True),
        }
    )

    @pre_load
    def process_category(self, data):
        category = data.get("category")
        if category:
            if isinstance(category, dict):
                category_name = category.get("name")
            else:
                category_name = category
            category_dict = {"name": category_name}
        else:
            category_dict = {}
        data["category"] = category_dict
        return data

    def is_locked(self, obj):
        if redis.hexists(locked_posts_redis_key, obj.id):
            try:
                lock_data = json.loads(redis.hget(locked_posts_redis_key, obj.id))
                expires = datetime.fromisoformat(lock_data["expires"])
                if expires >= datetime.now(pytz.utc):
                    return True
                else:
                    redis.hdel(locked_posts_redis_key, obj.id)  # clean up expired locks
                    PostBroadcast.unlocked(obj.id)
            except Exception:
                pass
        return False

    def get_locked_since(self, obj):
        if self.is_locked(obj):
            try:
                lock_data = json.loads(redis.hget(locked_posts_redis_key, obj.id))
                return lock_data["timestamp"]
            except:
                pass
        return None

    def get_lock_expires(self, obj):
        if self.is_locked(obj):
            try:
                lock_data = json.loads(redis.hget(locked_posts_redis_key, obj.id))
                return lock_data["expires"]
            except:
                pass
        return None

    def get_locked_by(self, obj):
        if self.is_locked(obj):
            try:
                lock_data = json.loads(redis.hget(locked_posts_redis_key, obj.id))
                user_schema = UserSchema(only=("id", "name", "email"))
                return user_schema.dump(User.query.get(lock_data["by_user_id"])).data
            except:
                pass
        return None


class ImageTagSchema(ma.Schema):
    class Meta:
        model = ImageTag

    tag = fields.Nested("TagSchema", only=("id", "name", "slug"))
    image = fields.Nested("ImageSchema", only=("id", "original_filename", "public_path", "links"))


class ImageSchema(ma.Schema):
    class Meta:
        model = Image

    id = fields.Integer(dump_only=True)
    title = fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255)
    public_path = fields.Method("get_public_path", dump_only=True)
    width = fields.Integer(dump_only=True)
    height = fields.Integer(dump_only=True)
    sizes = fields.List(fields.String(), dump_only=True)
    original_filename = fields.String(allow_none=True)
    data_url = fields.String(allow_none=True, load_only=True)
    author_id = fields.Integer(dump_only=True)
    tags = fields.Nested("ImageTagSchema", many=True, only=("tag",))
    posts = fields.Nested("PostImageSchema", many=True, exclude=("image",))
    created_at = fields.DateTime(format="iso8601")
    updated_at = fields.DateTime(format="iso8601")
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.image", id="<id>", _external=True),
            "collection": ma.URLFor("api.images", _external=True),
        }
    )

    def get_public_path(self, obj):
        date = obj.updated_at if obj.updated_at is not None else obj.created_at
        return "/" + "/".join(
            quote_plus(part.strip("/"), safe="/")
            for part in (
                current_app.config["PUBLIC_IMAGE_PATH"],
                str(date.year),
                str(date.month),
                str(date.day),
                obj.hash,
            )
        )


class TagSchema(ma.Schema):
    class Meta:
        model = Tag

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=lambda x: 0 < len(x) <= 255)
    slug = fields.String(dump_only=True)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.tag", id="<id>", _external=True),
            "collection": ma.URLFor("api.tags", _external=True),
            "relationships": {
                "posts": ma.URLFor("api.tag_posts", id="<id>", _external=True),
                "images": ma.URLFor("api.tag_images", id="<id>", _external=True),
            },
        }
    )
