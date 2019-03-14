from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_marshmallow import Marshmallow

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
    slug = fields.String()
    body = fields.String(required=True)
    body_html = fields.String()
    timestamp = fields.DateTime(format="iso8601")
    author = fields.Nested('UserSchema', only=['id', 'name', 'links'])
    links = ma.Hyperlinks({"self": ma.URLFor("api.post", id="<id>"), "collection": ma.URLFor("api.posts")})


class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    confirmed = fields.Boolean()
    name = fields.String(required=True, validate=validate.Length(3))
    location = fields.String()
    about_me = fields.String()
    member_since = fields.DateTime(format="iso8601")
    last_seen = fields.DateTime(format="iso8601")
    created_at = fields.DateTime(format="iso8601")
    role = fields.Nested('RoleSchema', only=['id', 'name', 'links'])
    posts = fields.Nested('PostSchema', many=True)
    links = ma.Hyperlinks({"self": ma.URLFor("api.user", id="<id>"), "collection": ma.URLFor("api.users")})


