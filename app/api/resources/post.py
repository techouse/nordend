from typing import List, Tuple

from dateutil import parser as dp
from flask import request, g
from sqlalchemy import desc, collate
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from ..broadcast.post import PostBroadcast
from ..helpers import PaginationHelper
from ..schemas import PostSchema
from ... import db, status
from ...models import Post, Category, User, PostCategory, PostAuthor

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
        if "sub_title" in request_dict and request_dict["sub_title"] is not None:
            post.sub_title = request_dict["sub_title"]
        if "slug" in request_dict:
            post_slug = request_dict["slug"]
            if Post.is_unique(id=id, category=post.category, slug=post_slug):
                post.slug = post_slug
            else:
                response = {"message": "A post with the same slug already exists"}
                return response, status.HTTP_400_BAD_REQUEST
        if "body" in request_dict:
            post.body = request_dict["body"]
        if "category_id" in request_dict:
            post.category = int(request_dict["category_id"])
        if "additional_category_ids" in request_dict:
            post.additional_categories = list(map(int, request_dict["additional_category_ids"]))
        if "tag_ids" in request_dict:
            post.tags = list(map(int, request_dict["tag_ids"]))
        if "related_ids" in request_dict:
            post.related = list(map(int, request_dict["related_ids"]))
        if "published" in request_dict and request_dict["published"] is not None:
            post.published = dp.parse(request_dict["published"])
        if "draft" in request_dict:
            post.draft = request_dict["draft"]
        if post.authors.filter(PostAuthor.user_id == g.current_user.id).count() == 0:
            post.authors.append(PostAuthor(user=g.current_user))
        dumped_post, dump_errors = post_schema.dump(post)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = post_schema.validate(dumped_post)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            post.update()
            updated_post = self.get(id)
            PostBroadcast.updated(post=post_schema.dump(updated_post).data, by_user_id=g.current_user.id)
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
            PostBroadcast.deleted(id, by_user_id=g.current_user.id)
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
        "sub_title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 1024),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "category_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
        "excluded_ids": fields.DelimitedList(fields.Integer),
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
        if "sub_title" in query_args:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["sub_title"])))
        if "slug" in query_args:
            filters.append(Post.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if "category_id" in query_args:
            filters.append(PostCategory.category_id == query_args["category_id"])
        if "author_id" in query_args:
            filters.append(PostAuthor.user_id == query_args["author_id"])
        if "created_at" in query_args:
            filters.append(Post.created_at == query_args["created_at"])
        if "excluded_ids" in query_args:
            filters.append(Post.id.notin_(query_args["excluded_ids"]))
        if filters:
            query = query.filter(*filters)

        # Apply sorting
        order_by = Post.id
        if "sort" in query_args and query_args["sort"]:
            column, direction = PaginationHelper.decode_sort(query_args["sort"])
            if column == "category.name":
                query = (
                    query.join(PostCategory, Post.categories)
                    .join(Category, PostCategory.category)
                    .filter(PostCategory.primary.is_(True))
                )
                order_by = Category.name
            elif column == "author.name":
                query = (
                    query.join(PostAuthor, Post.authors)
                    .join(User, PostAuthor.user)
                    .filter(PostAuthor.primary.is_(True))
                )
                order_by = User.name
            elif column in set(Post.__table__.columns.keys()):
                order_by = getattr(Post, column)
            order_by = collate(order_by, "NOCASE")
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
                author=g.current_user,
            )
            if "sub_title" in request_dict and request_dict["sub_title"]:
                post.sub_title = request_dict["sub_title"]
            if "category_id" in request_dict:
                post.category = int(request_dict["category_id"])
            if "additional_category_ids" in request_dict:
                post.additional_categories = list(map(int, request_dict["additional_category_ids"]))
            if "tag_ids" in request_dict:
                post.tags = list(map(int, request_dict["tag_ids"]))
            if "related_ids" in request_dict:
                post.related = list(map(int, request_dict["related_ids"]))
            if "published" in request_dict:
                post.published = dp.parse(request_dict["published"])
            if "draft" in request_dict:
                post.draft = request_dict["request_dict"]
            post.add(post)
            created_post = Post.query.get(post.id)
            result = post_schema.dump(created_post).data
            PostBroadcast.created(post=result, by_user_id=g.current_user.id)
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self):
        """ Bulk delete """
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        if "ids" in request_dict and (isinstance(request_dict["ids"], List) or isinstance(request_dict["ids"], Tuple)):
            ids = list(map(int, request_dict["ids"]))
            try:
                for id_ in ids:
                    post = Post.query.get(id_)
                    if post:
                        db.session.delete(post)
                        PostBroadcast.deleted(id_, by_user_id=g.current_user.id)
                db.session.commit()
                return {}, status.HTTP_204_NO_CONTENT
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"message": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
