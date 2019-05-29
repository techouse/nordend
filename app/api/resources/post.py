from flask import request, g
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from ..broadcast.post import PostBroadcast
from ..helpers import PaginationHelper
from ..schemas import PostSchema
from ... import db, status
from ...models import Post, Category, User

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
        if "category_id" in request_dict:
            post.category_id = request_dict["category_id"]
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
            updated_post = self.get(id)
            PostBroadcast.updated(post_schema.dump(updated_post).data)
            return updated_post
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
            PostBroadcast.deleted(id)
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return resp


class PostListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "sort": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "category_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args):
        query = Post.query

        # Apply filters
        filters = []
        if "search" in query_args and query_args["search"]:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["search"])))
        if "title" in query_args:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["title"])))
        if "slug" in query_args:
            filters.append(Post.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if "category_id" in query_args:
            filters.append(Post.category_id == query_args["category_id"])
        if "author_id" in query_args:
            filters.append(Post.author_id == query_args["author_id"])
        if "created_at" in query_args:
            filters.append(Post.created_at == query_args["created_at"])
        if filters:
            query = query.filter(*filters)

        # Apply sorting
        order_by = Post.id
        if "sort" in query_args and query_args["sort"]:
            column, direction = PaginationHelper.decode_sort(query_args["sort"])
            if column == "category.name":
                query = query.join(Category, Post.category)
                order_by = Category.name
            elif column == "author.name":
                query = query.join(User, Post.author)
                order_by = User.name
            elif column in set(Post.__table__.columns.keys()):
                order_by = getattr(Post, column)
            if direction == PaginationHelper.SORT_DESCENDING:
                order_by = desc(order_by)
            query = query.order_by(order_by)

        pagination_helper = PaginationHelper(
            request,
            query=query,
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
                author_id=g.current_user.id,
                category_id=request_dict["category_id"],
            )
            post.add(post)
            created_post = Post.query.get(post.id)
            result = post_schema.dump(created_post).data
            PostBroadcast.created(result)
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
