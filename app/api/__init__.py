from flask import Blueprint
from flask_restful import Api

from .resources.tag import TagListResource, TagResource, TagPostListResource, TagImageListResource
from .resources.csrf import CSRFResource
from .resources.image import ImageResource, ImageListResource
from .resources.authentication import (
    AuthenticationResource,
    ResetPasswordRequestResource,
    ResetPasswordResource,
    RegistrationResource,
    RegistrationConfirmationResource,
)
from .resources.category import CategoryListResource, CategoryResource, CategoryPostListResource
from .resources.post import PostListResource, PostResource
from .resources.role import RoleListResource, RoleResource, RoleUserListResource
from .resources.user import UserListResource, UserResource, UserPostListResource

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_bp)

api.add_resource(AuthenticationResource, "/login", endpoint="auth")
api.add_resource(RegistrationResource, "/register", endpoint="register")
api.add_resource(RegistrationConfirmationResource, "/confirm", endpoint="confirm")
api.add_resource(ResetPasswordRequestResource, "/reset_password_request", endpoint="reset_password_request")
api.add_resource(ResetPasswordResource, "/reset_password", endpoint="reset_password")
api.add_resource(CSRFResource, "/csrf", endpoint="csrf")

api.add_resource(RoleListResource, "/roles/", endpoint="roles")
api.add_resource(RoleResource, "/roles/<int:id>", endpoint="role")
api.add_resource(RoleUserListResource, "/roles/<int:id>/users/", endpoint="role_users")

api.add_resource(UserListResource, "/users/", endpoint="users")
api.add_resource(UserResource, "/users/<int:id>", endpoint="user")
api.add_resource(UserPostListResource, "/users/<int:id>/posts/", endpoint="user_posts")

api.add_resource(CategoryListResource, "/categories/", endpoint="categories")
api.add_resource(CategoryResource, "/categories/<int:id>", endpoint="category")
api.add_resource(CategoryPostListResource, "/categories/<int:id>/posts/", endpoint="category_posts")

api.add_resource(PostListResource, "/posts/", endpoint="posts")
api.add_resource(PostResource, "/posts/<int:id>", endpoint="post")

api.add_resource(ImageListResource, "/images/", endpoint="images")
api.add_resource(ImageResource, "/images/<int:id>", endpoint="image")

api.add_resource(TagListResource, "/tags/", endpoint="tags")
api.add_resource(TagResource, "/tags/<int:id>", endpoint="tag")
api.add_resource(TagPostListResource, "/tags/<int:id>/posts/", endpoint="tag_posts")
api.add_resource(TagImageListResource, "/tags/<int:id>/images/", endpoint="tag_images")

from . import broadcast as broadcast_events
