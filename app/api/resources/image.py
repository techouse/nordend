from hashlib import sha256
from io import BytesIO
from math import ceil
from os import makedirs
from os.path import join, dirname

from flask import request, g, current_app
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from webargs import fields
from webargs.flaskparser import use_args
from PIL import Image as PImage

from .authentication import TokenRequiredResource
from ..helpers import PaginationHelper
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
            image.delete(image)
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
            filters.append(Image.name.like("%{filter}%".format(filter=query_args["search"])))
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
            elif column in set(Post.__table__.columns.keys()):
                order_by = getattr(Post, column)
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
        if "file" not in request.files:
            response = {"message": "No file part"}
            return response, status.HTTP_400_BAD_REQUEST
        file = request.files.get("file")
        if file.filename == "":
            response = {"message": "No selected file"}
            return response, status.HTTP_400_BAD_REQUEST
        if file and allowed_image_file(file.filename):
            try:
                root_path = join(dirname(current_app.instance_path), 'app')
                digest = sha256(file.read()).hexdigest()
                path = join(current_app.config["PUBLIC_IMAGE_PATH"], digest)
                makedirs(join(root_path, path), exist_ok=True)
                original_image_path = join(root_path, path, "original.jpg")
                width, height = 0, 0
                sizes = []
                file.seek(0)
                with PImage.open(BytesIO(file.read())) as img:
                    width, height = img.size

                    if img.format == "JPEG":
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                    else:
                        fill_color = (255, 255, 255)  # make all transparent blocks white
                        img = img.convert("RGBA")
                        if img.mode in ('RGBA', 'LA'):
                            background = PImage.new(img.mode[:-1], img.size, fill_color)
                            background.paste(img, img.split()[-1])
                            img = background
                        img = img.convert("RGB")
                    img.save(original_image_path, quality=current_app.config["JPEG_COMPRESSION_QUALITY"])

                    for thumb_width in current_app.config["IMAGE_SIZES"]:
                        if width >= thumb_width:
                            if width == thumb_width:
                                img.save(join(root_path, path, "{}.jpg".format(thumb_width)),
                                         quality=current_app.config["JPEG_COMPRESSION_QUALITY"])
                            else:
                                thumb = img.copy()
                                thumb_height = int(ceil((thumb_width / width) * height))
                                thumb_size = thumb_width, thumb_height
                                thumb.thumbnail(thumb_size, PImage.LANCZOS)
                                thumb.save(join(root_path, path, "{}.jpg".format(thumb_width)),
                                           quality=current_app.config["JPEG_COMPRESSION_QUALITY"])
                            sizes.append(thumb_width)
                image = Image(
                    original_filename=file.filename,
                    path=digest,
                    author_id=g.current_user.id,
                    width=width,
                    height=height,
                    sizes=sizes
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


class ImagePostListResource(TokenRequiredResource):
    # TODO finish me
    pass
