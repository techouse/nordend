from itertools import combinations

from marshmallow import ValidationError

from ..models import Permission


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
