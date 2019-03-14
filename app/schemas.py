from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import validate

from .models import Post, User, Role

ma = Marshmallow()


class RoleSchema(ma.Schema):
    class Meta:
        model = Role

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    default = fields.Boolean(required=True)
    permissions = fields.Integer(required=True)
    links = ma.Hyperlinks({"self": ma.URLFor("api.role", id="<id>"), "collection": ma.URLFor("api.roles")})


class PostSchema(ma.Schema):
    class Meta:
        model = Post

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(1))
    slug = fields.String(allow_none=True)
    body = fields.String(required=True)
    body_html = fields.String(dump_only=True)
    timestamp = fields.DateTime(dump_only=True, format="iso8601")
    author = fields.Nested('UserSchema', dump_only=True, only=['id', 'name', 'links'])
    links = ma.Hyperlinks({"self": ma.URLFor("api.post", id="<id>"), "collection": ma.URLFor("api.posts")})


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
    role = fields.Nested('RoleSchema', only=['id', 'name', 'links'])
    posts = fields.Nested('PostSchema', dump_only=True, many=True)
    links = ma.Hyperlinks({"self": ma.URLFor("api.user", id="<id>"), "collection": ma.URLFor("api.users")})


