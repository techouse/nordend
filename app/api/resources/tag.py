from flask import request
from sqlalchemy import desc, String
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from .post import post_schema
from ..helpers import PaginationHelper
from ..schemas import TagSchema
from ... import db, status
from ...models import Tag, Post, Image

tag_schema = TagSchema()


class TagResource(TokenRequiredResource):
    def get(self, id):
        tag = Tag.query.get_or_404(id)
        result = tag_schema.dump(tag).data
        return result

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        tag = Tag.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = tag_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if "name" in request_dict:
                tag_name = request_dict["name"]
                if Tag.is_unique(id=0, name=tag_name):
                    tag.name = tag_name
                else:
                    response = {"message": "A tag with the same name already exists"}
                    return response, status.HTTP_400_BAD_REQUEST
            tag.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        tag = Tag.query.get_or_404(id)
        try:
            tag.delete(tag)
            resp = {}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_401_UNAUTHORIZED


class TagListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "sort": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "name": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
    }

    @use_args(get_args)
    def get(self, query_args):
        query = Tag.query

        filters = []
        if "search" in query_args and query_args["search"]:
            filters.append(Tag.name.like("%{filter}%".format(filter=query_args["search"])))
        if "name" in query_args:
            filters.append(Tag.name.like("%{filter}%".format(filter=query_args["name"])))
        if "slug" in query_args:
            filters.append(Tag.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if filters:
            query = query.filter(*filters)

        # Apply sorting
        order_by = Tag.id
        if "sort" in query_args and query_args["sort"]:
            column, direction = PaginationHelper.decode_sort(query_args["sort"])
            if column in set(Tag.__table__.columns.keys()):
                order_by = getattr(Tag, column)
            if direction == PaginationHelper.SORT_DESCENDING:
                order_by = desc(order_by)
            query = query.order_by(order_by)

        pagination_helper = PaginationHelper(
            request,
            query=query,
            resource_for_url="api.tags",
            key_name="results",
            schema=tag_schema,
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = tag_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        tag_name = request_dict["name"]
        if not Tag.is_unique(id=0, name=tag_name):
            response = {"message": "A tag with the same name already exists"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            tag = Tag(name=tag_name)
            tag.add(tag)
            query = Tag.query.get(tag.id)
            result = tag_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class TagPostListResource(TokenRequiredResource):
    get_args = {
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args, id):
        filters = []
        if "title" in query_args:
            filters.append(Post.title.like("%{filter}%".format(filter=query_args["title"])))
        if "slug" in query_args:
            filters.append(Post.slug.like("%{filter}%".format(filter=query_args["slug"])))
        if "author_id" in query_args:
            filters.append(Post.author_id == query_args["author_id"])
        if "created_at" in query_args:
            filters.append(Post.created_at == query_args["created_at"])

        pagination_helper = PaginationHelper(
            request,
            query=Tag.query.get(id).posts.filter(*filters),
            resource_for_url="api.tag_posts",
            key_name="results",
            schema=post_schema,
            url_parameters={"id": id},
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result


class TagImageListResource(TokenRequiredResource):
    get_args = {
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "slug": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: x > 0),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args, id):
        filters = []
        if "title" in query_args:
            filters.append(Image.title.like("%{filter}%".format(filter=query_args["title"])))
        if "original_filename" in query_args:
            filters.append(Image.original_filename.like("%{filter}%".format(filter=query_args["original_filename"])))
        if "size" in query_args:
            filters.append(Image.sizes.contains(query_args["size"]))
        if "created_at" in query_args:
            filters.append(Image.created_at == query_args["created_at"])

        pagination_helper = PaginationHelper(
            request,
            query=Tag.query.get(id).images.filter(*filters),
            resource_for_url="api.tag_images",
            key_name="results",
            schema=post_schema,
            url_parameters={"id": id},
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result
