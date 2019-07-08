from functools import wraps

import requests
from flask import abort, request, current_app, g
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def verify_recaptcha(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.recaptcha_valid = None

        if (
                request.method == "POST"
                and current_app.config["RECAPTCHA_SITE_KEY"]
                and current_app.config["RECAPTCHA_SECRET_KEY"]
        ):
            data = request.get_json() if request.get_json() else request.data
            recaptcha_token = data.get("recaptcha_token")
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

        return f(*args, **kwargs)

    return decorated_function
