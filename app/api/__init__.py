from flask import Blueprint
from flask_restful import Api

from .resources.role import RoleListResource, RoleResource
from .resources.post import PostListResource, PostResource
from .resources.user import UserListResource, UserResource

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_bp)

api.add_resource(RoleListResource, "/roles", endpoint="roles")
api.add_resource(RoleResource, "/roles/<int:id>", endpoint="role")
api.add_resource(UserListResource, "/users", endpoint="users")
api.add_resource(UserResource, "/users/<int:id>", endpoint="user")
api.add_resource(PostListResource, "/posts", endpoint="posts")
api.add_resource(PostResource, "/posts/<int:id>", endpoint="post")
