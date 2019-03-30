from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_load
from marshmallow import validate

from ..models import Post, User, Role, Category, Permission

ma = Marshmallow()


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
    permissions = fields.Integer(load_only=True,
                                 validate=lambda x: x >= 0 and Role.query.filter(Role.permissions == x).count() == 0)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.role", id="<id>", _external=True),
            "collection": ma.URLFor("api.roles", _external=True),
            "relationships": {
                "users": ma.URLFor("api.role_users", id="<id>", _external=True),
            }
        }
    )


class CategorySchema(ma.Schema):
    class Meta:
        model = Category

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=lambda x: 0 < len(x) <= 255)
    slug = fields.String(dump_only=True)
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.category", id="<id>", _external=True),
            "collection": ma.URLFor("api.categories", _external=True),
            "relationships": {
                "posts": ma.URLFor("api.category_posts", id="<id>", _external=True),
            }
        }
    )


class PostSchema(ma.Schema):
    class Meta:
        model = Post

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=lambda x: 0 < len(x) <= 255)
    slug = fields.String(dump_only=True)
    body = fields.String(required=True, validate=lambda x: 0 <= len(x) <= 2 ** 16)
    body_html = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format="iso8601")
    updated_at = fields.DateTime(dump_only=True, format="iso8601")
    author = fields.Nested("UserSchema", dump_only=True, exclude=("posts",))
    category_id = fields.Integer(required=True,
                                 validate=lambda x: x >= 0 and Category.query.get(x) is not None)
    category = fields.Nested("CategorySchema", dump_only=True, exclude=("posts",))
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
            category_dict = dict(name=category_name)
        else:
            category_dict = {}
        data["category"] = category_dict
        return data


class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(load_only=True, validate=lambda x: 8 <= len(x) <= 128)
    confirmed = fields.Boolean(required=True)
    name = fields.String(required=True, validate=validate.Length(3))
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
            "relationships": {
                "posts": ma.URLFor("api.user_posts", id="<id>", _external=True),
            }
        }
    )
