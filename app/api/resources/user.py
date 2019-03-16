from flask import request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError

from .authentication import TokenRequiredResource
from ..helpers import PaginationHelper
from ..schemas import UserSchema
from ... import db, status
from ...models import User

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
            response = {"error": "No input data provided"}
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
                    response = {"error": "A user with the same e-mail address already exists"}
                    return response, status.HTTP_400_BAD_REQUEST
            if "password" in request_dict:
                user.password = request_dict["password"]
            if "confirmed" in request_dict:
                user.confirmed = request_dict["confirmed"]
            if "name" in request_dict:
                user.name = request_dict["name"]
            if "location" in request_dict:
                user.location = request_dict["location"]
            if "about_me" in request_dict:
                user.about_me = request_dict["location"]
            user.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            user.delete(user)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class UserListResource(TokenRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=User.query, resource_for_url="api.users", key_name="results", schema=user_schema
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
            response = {"error": "A user with the same e-mail address already exists"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            user = User(
                name=request_dict["name"],
                email=request_dict["email"],
                password=request_dict["password"],
                confirmed=request_dict["confirmed"] if "confirmed" in request_dict else "",
                location=request_dict["location"] if "location" in request_dict else "",
                about_me=request_dict["about_me"] if "about_me" in request_dict else "",
            )
            user.add(user)
            query = User.query.get(user.id)
            result = user_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
