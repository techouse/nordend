from flask import request
from ..helpers import PaginationHelper
from flask_restful import Resource

from ...models import User
from ...schemas import UserSchema

user_schema = UserSchema()


class UsersResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=User.query, resource_for_url="api.users", key_name="data", schema=user_schema
        )
        result = pagination_helper.paginate_query()
        return result


class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        result = user_schema.dump(user).data
        return {"data": result}
