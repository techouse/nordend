from flask import render_template, request
from .. import db
from . import errors
from ..api.errors import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]


@errors.app_errorhandler(400)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(400, str(error))
    return render_template("errors/400.html"), 400


@errors.app_errorhandler(403)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(403, str(error))
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404, str(error))
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(405)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(405, str(error))
    return render_template("errors/405.html"), 405


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500, str(error))
    return render_template("errors/500.html"), 500
