from flask import request
from ..helpers import PaginationHelper
from flask_restful import Resource

from ...models import Role
from ...schemas import RoleSchema

role_schema = RoleSchema()


class RolesResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=Role.query, resource_for_url="api.roles", key_name="data", schema=role_schema
        )
        result = pagination_helper.paginate_query()
        return result


class RoleResource(Resource):
    def get(self, id):
        role = Role.query.get_or_404(id)
        result = role_schema.dump(role).data
        return {"data": result}
