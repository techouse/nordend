from flask import request
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields, validate
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from .user import user_schema
from ..helpers import PaginationHelper
from ..schemas import RoleSchema
from ... import status, db
from ...models import Role, User

role_schema = RoleSchema()


class RoleResource(TokenRequiredResource):
    def get(self, id):
        role = Role.query.get_or_404(id)
        result = role_schema.dump(role).data
        return result

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        role = Role.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = role_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if "name" in request_dict:
                role_name = request_dict["name"]
                if Role.is_unique(id=0, name=role_name):
                    role.name = role_name
                else:
                    response = {"message": "A role with the same name already exists"}
                    return response, status.HTTP_400_BAD_REQUEST
            role.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        role = Role.query.get_or_404(id)
        try:
            role.delete(role)
            resp = {}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_401_UNAUTHORIZED


class RoleListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "sort": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "name": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 64),
        "default": fields.Boolean(allow_none=True),
        "permissions": fields.Integer(allow_none=True, validate=lambda x: x > 0),
    }

    @use_args(get_args)
    def get(self, query_args):
        query = Role.query

        filters = []
        if "search" in query_args and query_args["search"]:
            filters.append(Role.name.like("%{filter}%".format(filter=query_args["search"])))
        if "name" in query_args:
            filters.append(Role.name.like("%{filter}%".format(filter=query_args["name"])))
        if "default" in query_args:
            filters.append(Role.default == query_args["default"])
        if "permissions" in query_args:
            filters.append(Role.permissions == query_args["permissions"])
        if filters:
            query = query.filter(*filters)

        # Apply sorting
        order_by = Role.id
        if "sort" in query_args and query_args["sort"]:
            column, direction = PaginationHelper.decode_sort(query_args["sort"])
            if column in set(Role.__table__.columns.keys() + ["follow", "comment", "write", "moderate", "admin"]):
                order_by = getattr(Role, column)
            if direction == PaginationHelper.SORT_DESCENDING:
                order_by = desc(order_by)
            query = query.order_by(order_by)

        pagination_helper = PaginationHelper(
            request,
            query=query,
            resource_for_url="api.roles",
            key_name="results",
            schema=role_schema,
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = role_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        role_name = request_dict["name"]
        if not Role.is_unique(id=0, name=role_name):
            response = {"message": "A role with the same name already exists"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            role = Role(
                name=role_name,
                default=request_dict["default"] if "default" in request_dict else False,
                permissions=request_dict["permissions"] if "permissions" in request_dict else 0
            )
            role.add(role)
            query = Role.query.get(role.id)
            result = role_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class RoleUserListResource(TokenRequiredResource):
    get_args = {
        "name": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "email": fields.Email(allow_none=True, validate=validate.Email()),
        "location": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "confirmed": fields.Boolean(),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args, id):
        filters = [User.role_id == id]
        if "name" in query_args:
            filters.append(User.name.like("%{filter}%".format(filter=query_args["name"])))
        if "email" in query_args:
            filters.append(User.email.like("%{filter}%".format(filter=query_args["email"])))
        if "location" in query_args:
            filters.append(User.location.like("%{filter}%".format(filter=query_args["location"])))
        if "confirmed" in query_args:
            filters.append(User.confirmed == query_args["confirmed"])
        if "created_at" in query_args:
            filters.append(User.created_at == query_args["created_at"])

        pagination_helper = PaginationHelper(
            request,
            query=User.query.filter(*filters),
            resource_for_url="api.role_users",
            key_name="results",
            schema=user_schema,
            url_parameters={"id": id},
        )
        result = pagination_helper.paginate_query()
        return result
