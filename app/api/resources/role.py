from flask import request
from sqlalchemy import desc
from webargs import fields, validate
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from .user import user_schema
from ..helpers import PaginationHelper
from ..schemas import RoleSchema
from ... import status
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
        resp = {"message": "Method not implemented"}
        return resp, status.HTTP_501_NOT_IMPLEMENTED

    def delete(self, id):
        resp = {"message": "Method not implemented"}
        return resp, status.HTTP_501_NOT_IMPLEMENTED


class RoleListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "sort": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "name": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 64),
        "default": fields.Boolean(allow_none=True, ),
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
        resp = {"message": "Method not implemented"}
        return resp, status.HTTP_501_NOT_IMPLEMENTED


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
