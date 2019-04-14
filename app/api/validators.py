from itertools import combinations

from marshmallow import ValidationError, validate

from flask import current_app
from ..models import Permission, User


def valid_permission(value):
    if not value:
        raise ValidationError("Permission not provided.")
    else:
        permissions = [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        permission_combinations = []
        for x in range(1, len(permissions) + 1):
            permission_combinations += combinations(permissions, x)

        if value not in set([sum(permission_combination) for permission_combination in permission_combinations]):
            raise ValidationError("Invalid permission.")


def valid_password_reset_token(value):
    if not value:
        raise ValidationError("Reset token not provided.")
    else:
        if not User.verify_reset_password_token(value):
            raise ValidationError("Invalid reset token")


def allowed_image_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
