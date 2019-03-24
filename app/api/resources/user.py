from flask import request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields, validate
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from .post import post_schema
from ..helpers import PaginationHelper
from ..schemas import UserSchema
from ... import db, status
from ...models import User, Post, Role

user_schema = UserSchema()


class UserResource(TokenRequiredResource):
    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return result

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        user = User.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = user_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if "email" in request_dict:
                user_email = request_dict["email"]
                if User.is_unique(id=id, email=user_email):
                    user.email = user_email
                else:
                    response = {"message": "A user with the same e-mail address already exists"}
                    return response, status.HTTP_400_BAD_REQUEST
            if "password" in request_dict:
                user.password = request_dict["password"]
            if "role_id" in request_dict:
                role_id = request_dict["role_id"]
                if Role.query.get(role_id):
                    user.role_id = role_id
                else:
                    response = {"message": "A role with that ID does not exist!"}
                    return response, status.HTTP_400_BAD_REQUEST
            if "confirmed" in request_dict:
                user.confirmed = request_dict["confirmed"]
            if "name" in request_dict:
                user.name = request_dict["name"]
            if "location" in request_dict:
                user.location = request_dict["location"]
            if "about_me" in request_dict:
                user.about_me = request_dict["about_me"]
            user.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            user.delete(user)
            resp = {}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class UserListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "name": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "email": fields.Email(allow_none=True, validate=validate.Email()),
        "location": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "confirmed": fields.Boolean(allow_none=True),
        "role_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args):
        filters = []
        if "search" in query_args and query_args["search"]:
            filters.append(or_(
                User.name.like("%{filter}%".format(filter=query_args["search"])),
                User.email.like("%{filter}%".format(filter=query_args["search"]))
            ))
        if "name" in query_args and query_args["name"]:
            filters.append(User.name.like("%{filter}%".format(filter=query_args["name"])))
        if "email" in query_args and query_args["email"]:
            filters.append(User.email.like("%{filter}%".format(filter=query_args["email"])))
        if "location" in query_args and query_args["location"]:
            filters.append(User.location.like("%{filter}%".format(filter=query_args["location"])))
        if "confirmed" in query_args:
            filters.append(User.confirmed == query_args["confirmed"])
        if "role_id" in query_args and query_args["role_id"]:
            filters.append(User.role_id == query_args["role_id"])
        if "created_at" in query_args and query_args["created_at"]:
            filters.append(User.created_at == query_args["created_at"])

        pagination_helper = PaginationHelper(
            request,
            query=User.query.filter(*filters) if filters else User.query,
            resource_for_url="api.users",
            key_name="results",
            schema=user_schema,
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {"message": "No input data provided"}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = user_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        user_email = request_dict["email"]
        if not User.is_unique(id=0, email=user_email):
            response = {"message": "A user with the same e-mail address already exists"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            user = User(
                name=request_dict["name"],
                email=request_dict["email"],
                password=request_dict["password"],
                confirmed=request_dict["confirmed"] if "confirmed" in request_dict else False,
                location=request_dict["location"] if "location" in request_dict else "",
                about_me=request_dict["about_me"] if "about_me" in request_dict else "",
            )
            user.add(user)
            query = User.query.get(user.id)
            result = user_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class UserPostListResource(TokenRequiredResource):
    get_args = {
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "category_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args, id):
        filters = [Post.author_id == id]
        if "title" in query_args:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["title"])))
        if "slug" in query_args:
            filters.append(Post.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if "category_id" in query_args:
            filters.append(Post.category_id == query_args["category_id"])
        if "created_at" in query_args:
            filters.append(Post.created_at == query_args["created_at"])

        pagination_helper = PaginationHelper(
            request,
            query=Post.query.filter(*filters),
            resource_for_url="api.user_posts",
            key_name="results",
            schema=post_schema,
            url_parameters={"id": id},
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result
