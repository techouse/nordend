from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_load
from marshmallow import validate

from ..models import Post, User, Role, Category

ma = Marshmallow()


class RoleSchema(ma.Schema):
    class Meta:
        model = Role

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    default = fields.Boolean(required=True)
    permissions = fields.Integer(required=True)
    users = fields.Nested("UserSchema", dump_only=True, many=True, exclude=("posts", "role"))
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.role", id="<id>", _external=True),
            "collection": ma.URLFor("api.roles", _external=True),
        }
    )


class CategorySchema(ma.Schema):
    class Meta:
        model = Category

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    slug = fields.String(dump_only=True)
    posts = fields.Nested("PostSchema", dump_only=True, many=True, exclude=("category", "author"))
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.categories", id="<id>", _external=True),
            "collection": ma.URLFor("api.categories", _external=True),
        }
    )


class PostSchema(ma.Schema):
    class Meta:
        model = Post

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(1))
    slug = fields.String(dump_only=True)
    body = fields.String(required=True)
    body_html = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format="iso8601")
    updated_at = fields.DateTime(dump_only=True, format="iso8601")
    author = fields.Nested("UserSchema", dump_only=True, exclude=("posts",))
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
    password = fields.String(load_only=True, validate=validate.Length(8))
    confirmed = fields.Boolean(allow_none=True)
    name = fields.String(required=True, validate=validate.Length(3))
    location = fields.String(allow_none=True)
    about_me = fields.String(allow_none=True)
    member_since = fields.DateTime(dump_only=True, format="iso8601")
    last_seen = fields.DateTime(dump_only=True, format="iso8601")
    created_at = fields.DateTime(dump_only=True, format="iso8601")
    updated_at = fields.DateTime(dump_only=True, format="iso8601")
    role = fields.Nested("RoleSchema", exclude=("users",))
    posts = fields.Nested("PostSchema", dump_only=True, many=True, exclude=("author",))
    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.user", id="<id>", _external=True),
            "collection": ma.URLFor("api.users", _external=True),
        }
    )
