from flask import Blueprint
from flask_restful import Api

from .resources.role import RolesResource, RoleResource
from .resources.post import PostsResource, PostResource
from .resources.user import UsersResource, UserResource

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_bp)

api.add_resource(RolesResource, "/roles", endpoint="roles")
api.add_resource(RoleResource, "/roles/<int:id>", endpoint="role")
api.add_resource(UsersResource, "/users", endpoint="users")
api.add_resource(UserResource, "/users/<int:id>", endpoint="user")
api.add_resource(PostsResource, "/posts", endpoint="posts")
api.add_resource(PostResource, "/posts/<int:id>", endpoint="post")
