from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

from .. import status
from ..authentication import TokenRequiredResource
from ..helpers import PaginationHelper
from ..schemas import PostSchema
from ... import db
from ...models import Post

post_schema = PostSchema()


class PostResource(TokenRequiredResource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        result = post_schema.dump(post).data
        return result

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        post = Post.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"error": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        if "title" in request_dict:
            post.title = request_dict["title"]
        if "slug" in request_dict:
            post_slug = request_dict["slug"]
            if Post.is_unique(id=id, category=post.category, slug=post_slug):
                post.slug = post_slug
            else:
                response = {"error": "A post with the same slug already exists"}
                return response, status.HTTP_400_BAD_REQUEST
        if "body" in request_dict:
            post.body = request_dict["body"]
        dumped_post, dump_errors = post_schema.dump(post)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = post_schema.validate(dumped_post)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            post.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        post = Post.query.get_or_404(id)
        try:
            post.delete(post)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class PostListResource(TokenRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=Post.query, resource_for_url="api.posts", key_name="results", schema=post_schema
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"error": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = post_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            post = Post(
                title=request_dict["title"],
                body=request_dict["body"],
                slug=request_dict["slug"] if "slug" in request_dict else "",
            )
            post.add(post)
            query = Post.query.get(post.id)
            result = post_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
