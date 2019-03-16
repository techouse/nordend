from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from . import api_bp
from . import status
from ..exceptions import ValidationError


def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(status.HTTP_400_BAD_REQUEST, message)


def unauthorized(message):
    return error_response(status.HTTP_401_UNAUTHORIZED, message)


def forbidden(message):
    return error_response(status.HTTP_403_FORBIDDEN, message)


@api_bp.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
