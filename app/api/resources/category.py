from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .post import post_schema
from .authentication import TokenRequiredResource
from ..helpers import PaginationHelper
from ..schemas import CategorySchema
from ... import db, status
from ...models import Category, Post

category_schema = CategorySchema()


class CategoryResource(TokenRequiredResource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        result = category_schema.dump(category).data
        return {"data": result}

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        category = Category.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"error": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if "name" in request_dict:
                category_name = request_dict["name"]
                if Category.is_unique(id=0, name=category_name):
                    category.name = category_name
                else:
                    response = {"error": "A category with the same name already exists"}
                    return response, status.HTTP_400_BAD_REQUEST
            category.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        category = Category.query.get_or_404(id)
        try:
            category.delete(category)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class CategoryListResource(TokenRequiredResource):
    get_args = {
        "name": fields.String(validate=lambda x: 0 < len(x) <= 255),
        "slug": fields.String(validate=lambda x: 0 < len(x) <= 255),
    }

    @use_args(get_args)
    def get(self, query_args):
        filters = []
        if "name" in query_args:
            filters.append(Category.name.like("%{filter}%".format(filter=query_args["name"])))
        if "slug" in query_args:
            filters.append(Category.slug.like("%{filter}%".format(filter=query_args["slug"])))

        pagination_helper = PaginationHelper(
            request,
            query=Category.query.filter(*filters) if filters else Category.query,
            resource_for_url="api.categories",
            key_name="results",
            schema=category_schema,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {"error": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        category_name = request_dict["name"]
        if not Category.is_unique(id=0, name=category_name):
            response = {"error": "A category with the same name already exists"}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            category = Category(title=category_name)
            category.add(category)
            query = Category.query.get(category.id)
            result = category_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class CategoryPostListResource(TokenRequiredResource):
    get_args = {
        "title": fields.String(validate=lambda x: 0 < len(x) <= 255),
        "slug": fields.String(validate=lambda x: 0 < len(x) <= 255),
        "author_id": fields.Integer(validate=lambda x: x > 0),
        "created_at": fields.DateTime(format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args, id):
        filters = [Post.category_id == id]
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
            query=Post.query.filter(*filters),
            resource_for_url="api.category_posts",
            key_name="results",
            schema=post_schema,
            url_parameters={"id": id},
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result
