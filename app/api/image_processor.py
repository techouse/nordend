from datetime import datetime
from hashlib import sha256, md5
from io import BytesIO
from math import ceil
from os import makedirs
from os.path import join, dirname
from shutil import copy2

import pytz
from PIL import Image as PImage
from flask import current_app


class ImageProcessor:
    @staticmethod
    def process(file, filename=None):
        root_path = join(dirname(current_app.instance_path), "app")
        digest = sha256(file.read()).hexdigest()
        if filename is None:
            try:
                filename = file.filename
            except AttributeError:
                filename = "{}.jpg".format(md5(file.read()).hexdigest())
        local_datetime = datetime.now(pytz.utc).astimezone(current_app.config["TIMEZONE"])
        path = join(
            current_app.config["PUBLIC_IMAGE_PATH"],
            str(local_datetime.year),
            str(local_datetime.month),
            str(local_datetime.day),
            digest,
        )
        makedirs(join(root_path, path), exist_ok=True)
        original_image_path = join(root_path, path, "original.jpg")
        width, height = 0, 0
        sizes = []
        file.seek(0)
        with PImage.open(file if isinstance(file, BytesIO) else BytesIO(file.read())) as img:
            width, height = img.size
            if img.format == "JPEG":
                if img.mode != "RGB":
                    img = img.convert("RGB")
            else:
                fill_color = (255, 255, 255)  # make all transparent blocks white
                img = img.convert("RGBA")
                if img.mode in ("RGBA", "LA"):
                    background = PImage.new(img.mode[:-1], img.size, fill_color)
                    background.paste(img, img.split()[-1])
                    img = background
                img = img.convert("RGB")
            img.save(original_image_path, quality=current_app.config["JPEG_COMPRESSION_QUALITY"])
            # create thumbs
            for thumb_width in current_app.config["IMAGE_SIZES"]:
                if width >= thumb_width:
                    if width == thumb_width:
                        copy2(original_image_path, join(root_path, path, "{}.jpg".format(thumb_width)))
                    else:
                        thumb = img.copy()
                        thumb_height = int(ceil((thumb_width / width) * height))
                        thumb_size = thumb_width, thumb_height
                        thumb.thumbnail(thumb_size, PImage.LANCZOS)
                        thumb.save(
                            join(root_path, path, "{}.jpg".format(thumb_width)),
                            quality=current_app.config["JPEG_COMPRESSION_QUALITY"],
                        )
                    sizes.append(thumb_width)
            return dict(
                original_filename=filename,
                hash=digest,
                width=width,
                height=height,
                sizes=sizes,
                created_at=local_datetime
            )
