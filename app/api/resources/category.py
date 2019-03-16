from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ... import db
from .. import status
from ..helpers import PaginationHelper
from flask_restful import Resource

from ...models import Category
from ..schemas import CategorySchema

category_schema = CategorySchema()


class CategoryResource(Resource):
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
                category.name = request_dict["name"]
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


class CategoryListResource(Resource):
    def get(self):
        pagination_helper = PaginationHelper(
            request, query=Category.query, resource_for_url="api.categories", key_name="data", schema=category_schema
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
        try:
            category = Category(title=request_dict["title"].strip())
            category.add(category)
            query = Category.query.get(category.id)
            result = category_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
