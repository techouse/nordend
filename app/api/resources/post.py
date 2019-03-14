from flask import request
from ..helpers import PaginationHelper
from flask_restful import Resource

from ...models import Post
from ...schemas import PostSchema

post_schema = PostSchema()


class PostListResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=Post.query, resource_for_url="api.posts", key_name="data", schema=post_schema
        )
        result = pagination_helper.paginate_query()
        return result


class PostResource(Resource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        result = post_schema.dump(post).data
        return {"data": result}
