from flask import request, make_response
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from ..helpers import PaginationHelper
from ..schemas import PostSchema
from ... import db, status
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
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        if "title" in request_dict:
            post.title = request_dict["title"]
        if "slug" in request_dict:
            post_slug = request_dict["slug"]
            if Post.is_unique(id=id, category=post.category, slug=post_slug):
                post.slug = post_slug
            else:
                response = {"message": "A post with the same slug already exists"}
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
            resp = {"message": str(e)}
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return resp

    def delete(self, id):
        post = Post.query.get_or_404(id)
        try:
            post.delete(post)
            resp = {}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return resp


class PostListResource(TokenRequiredResource):
    get_args = {
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "category_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args):
        filters = []
        if "title" in query_args:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["title"])))
        if "slug" in query_args:
            filters.append(Post.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if "category_id" in query_args:
            filters.append(Post.category_id)
        if "author_id" in query_args:
            filters.append(Post.author_id)
        if "created_at" in query_args:
            filters.append(Post.created_at)

        pagination_helper = PaginationHelper(
            request,
            query=Post.query.filter(*filters) if filters else Post.query,
            resource_for_url="api.posts",
            key_name="results",
            schema=post_schema,
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
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
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
