import re
from base64 import b64decode
from binascii import Error as BinasciiError
from hashlib import sha256, md5
from io import BytesIO
from os.path import join, dirname, isdir
from shutil import rmtree
from typing import List, Tuple

from flask import request, g, current_app
from sqlalchemy import desc, or_, collate
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args

from .authentication import TokenRequiredResource
from ..helpers import PaginationHelper
from ..image_processor import ImageProcessor
from ..schemas import ImageSchema
from ..validators import allowed_image_file
from ... import db, status
from ...models import Post, Image, User

image_schema = ImageSchema()


class ImageResource(TokenRequiredResource):
    def get(self, id):
        image = Image.query.get_or_404(id)
        result = image_schema.dump(image).data
        return result

    def put(self, id):
        return self.patch(id)

    def patch(self, id):
        image = Image.query.get_or_404(id)
        request_dict = request.get_json()
        if not request_dict:
            response = {"message": "No input data provided"}
            return response, status.HTTP_400_BAD_REQUEST
        errors = image_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        if "title" in request_dict and request_dict["title"]:
            image.title = request_dict["title"]
        if "tag_ids" in request_dict:
            image.tags = list(map(int, request_dict["tag_ids"]))
        if "data_url" in request_dict and request_dict["data_url"]:
            image_data = re.sub("^data:image/.+;base64,", "", request_dict["data_url"])
            if image_data:
                file = BytesIO(b64decode(image_data))
                filename = request_dict.get("original_filename")
                if not filename:
                    filename = "{}.jpg".format(md5(file.read()).hexdigest())
                try:
                    processed_image = ImageProcessor.process(file, filename=filename)
                    image.hash = processed_image["hash"]
                    image.width = processed_image["width"]
                    image.height = processed_image["height"]
                    image.sizes = processed_image["sizes"]
                except BinasciiError as e:
                    resp = {"message": str(e)}
                    return resp, status.HTTP_400_BAD_REQUEST
        try:
            image.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        image = Image.query.get_or_404(id)
        try:
            date = image.updated_at if image.updated_at is not None else image.created_at
            path = join(
                join(dirname(current_app.instance_path), "app"),
                join(
                    current_app.config["PUBLIC_IMAGE_PATH"], str(date.year), str(date.month), str(date.day), image.hash
                ),
            )
            image.delete(image)
            if isdir(path):
                rmtree(path)
            resp = {}
            return resp, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"message": str(e)}
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return resp


class ImageListResource(TokenRequiredResource):
    get_args = {
        "search": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "sort": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "title": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 64),
        "original_filename": fields.String(allow_none=True, validate=lambda x: 0 <= len(x) <= 255),
        "author_id": fields.Integer(allow_none=True, validate=lambda x: User.query.get(x) is not None),
        "post_id": fields.Integer(allow_none=True, validate=lambda x: Post.query.get(x) is not None),
        "created_at": fields.DateTime(allow_none=True, format="iso8601"),
    }

    @use_args(get_args)
    def get(self, query_args):
        query = Image.query

        # Apply filters
        filters = []
        if "search" in query_args and query_args["search"]:
            filters.append(
                or_(
                    Image.title.like("%{filter}%".format(filter=query_args["search"])),
                    Image.original_filename.like("%{filter}%".format(filter=query_args["search"])),
                )
            )
        if "title" in query_args:
            filters.append(Image.title.like("%{filter}%".format(filter=query_args["title"])))
        if "original_filename" in query_args:
            filters.append(Image.original_filename.like("%{filter}%".format(filter=query_args["original_filename"])))
        if "author_id" in query_args:
            filters.append(Post.author_id == query_args["author_id"])
        if "post_id" in query_args:
            filters.append(Post.post_id == query_args["post_id"])
        if "created_at" in query_args:
            filters.append(Post.created_at == query_args["created_at"])
        if filters:
            query = query.filter(*filters)

        # Apply sorting
        order_by = Image.id
        if "sort" in query_args and query_args["sort"]:
            column, direction = PaginationHelper.decode_sort(query_args["sort"])
            if column == "post.name":
                query = query.join(Post, Image.post)
                order_by = Post.name
            elif column == "author.name":
                query = query.join(User, Image.author)
                order_by = User.name
            elif column in set(Image.__table__.columns.keys()):
                order_by = getattr(Image, column)
            order_by = collate(order_by, "NOCASE")
            if direction == PaginationHelper.SORT_DESCENDING:
                order_by = desc(order_by)
            query = query.order_by(order_by)

        pagination_helper = PaginationHelper(
            request,
            query=query,
            resource_for_url="api.images",
            key_name="results",
            schema=image_schema,
            query_args=query_args,
        )
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if "file" in request.files:
            file = request.files.get("file")
            filename = file.filename
            if filename == "":
                response = {"message": "No selected file"}
                return response, status.HTTP_400_BAD_REQUEST
        elif "data_url" in request_dict and request_dict["data_url"]:
            image_data = re.sub("^data:image/.+;base64,", "", request_dict["data_url"])
            if image_data:
                file = BytesIO(b64decode(image_data))
                filename = request_dict.get("original_filename")
                if not filename:
                    filename = "{}.jpg".format(md5(file.read()).hexdigest())
            else:
                response = {"message": "Invalid image_data priovided"}
                return response, status.HTTP_400_BAD_REQUEST
        else:
            response = {"message": "No image provided"}
            return response, status.HTTP_400_BAD_REQUEST
        if file and allowed_image_file(filename):
            try:
                digest = sha256(file.read()).hexdigest()
                file.seek(0)
                root_path = join(dirname(current_app.instance_path), "app")
                if Image.query.filter_by(hash=digest).count() > 0:
                    for image in Image.query.filter_by(hash=digest).all():
                        image_path = join(
                            root_path,
                            current_app.config["PUBLIC_IMAGE_PATH"],
                            str(image.created_at.year),
                            str(image.created_at.month),
                            str(image.created_at.day),
                            digest,
                        )
                        if isdir(image_path):
                            # Return first existing image
                            result = image_schema.dump(image).data
                            return result, status.HTTP_200_OK
                        else:
                            # Image does not exist so we delete it from the database
                            image.delete(image)
                processed_image = ImageProcessor.process(file)
                image = Image(
                    original_filename=processed_image["original_filename"],
                    hash=processed_image["hash"],
                    author_id=g.current_user.id,
                    width=processed_image["width"],
                    height=processed_image["height"],
                    sizes=processed_image["sizes"],
                    created_at=processed_image["created_at"],
                )
                image.add(image)
                query = Image.query.get(image.id)
                result = image_schema.dump(query).data
                return result, status.HTTP_201_CREATED
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"message": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
            except Exception as e:
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
                    image = Image.query.get(id_)
                    if image:
                        date = image.updated_at if image.updated_at is not None else image.created_at
                        path = join(
                            join(dirname(current_app.instance_path), "app"),
                            join(
                                current_app.config["PUBLIC_IMAGE_PATH"],
                                str(date.year),
                                str(date.month),
                                str(date.day),
                                image.hash,
                            ),
                        )
                        db.session.delete(image)
                        if isdir(path):
                            rmtree(path)
                db.session.commit()
                return {}, status.HTTP_204_NO_CONTENT
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"message": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST


class ImagePostListResource(TokenRequiredResource):
    # TODO finish me
    pass
