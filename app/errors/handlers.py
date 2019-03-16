from flask import render_template, request
from .. import db, status
from . import errors
from ..api.errors import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]


@errors.app_errorhandler(status.HTTP_400_BAD_REQUEST)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(status.HTTP_400_BAD_REQUEST, str(error))
    return render_template("errors/400.html"), status.HTTP_400_BAD_REQUEST


@errors.app_errorhandler(status.HTTP_403_FORBIDDEN)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(status.HTTP_403_FORBIDDEN, str(error))
    return render_template("errors/403.html"), status.HTTP_403_FORBIDDEN


@errors.app_errorhandler(status.HTTP_404_NOT_FOUND)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(status.HTTP_404_NOT_FOUND, str(error))
    return render_template("errors/404.html"), status.HTTP_404_NOT_FOUND


@errors.app_errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(status.HTTP_405_METHOD_NOT_ALLOWED, str(error))
    return render_template("errors/405.html"), status.HTTP_405_METHOD_NOT_ALLOWED


@errors.app_errorhandler(status.HTTP_422_UNPROCESSABLE_ENTITY)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, str(error))
    return render_template("errors/422.html"), status.HTTP_422_UNPROCESSABLE_ENTITY


@errors.app_errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))
    return render_template("errors/500.html"), status.HTTP_500_INTERNAL_SERVER_ERROR
