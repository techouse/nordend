from functools import wraps

import requests
from flask import abort, request, current_app, g
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if not g.current_user.can(permission):
                    abort(403)
                return f(*args, **kwargs)
            except AttributeError:
                abort(403)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def staff_required(f):
    return permission_required(Permission.MODERATE)(f)


def author_required(f):
    return permission_required(Permission.WRITE)(f)


def verify_recaptcha(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.recaptcha_valid = None

        if (
                request.method == "POST"
                and current_app.config["RECAPTCHA_SITE_KEY"]
                and current_app.config["RECAPTCHA_SECRET_KEY"]
        ):
            request_data = request.get_json() if request.get_json() else request.data
            try:
                recaptcha_token = request_data.get("recaptcha_token")
                if recaptcha_token:
                    r = requests.post(
                        "https://www.google.com/recaptcha/api/siteverify",
                        data={
                            "secret": current_app.config["RECAPTCHA_SECRET_KEY"],
                            "response": recaptcha_token,
                            "remoteip": request.access_route[0],
                        },
                    )
                    result = r.json()
                    g.recaptcha_valid = result.get("success") or False
                else:
                    g.recaptcha_valid = False
            except AttributeError:
                g.recaptcha_valid = False

        return f(*args, **kwargs)

    return decorated_function
