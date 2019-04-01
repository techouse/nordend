from urllib.parse import urljoin

from flask import current_app, url_for

from ..email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        user.email,
        "[{app_name}] Reset Your Password".format(app_name=current_app.config["APP_NAME"]),
        "api/auth/email/reset_password",
        user=user,
        token=token,
        app_name=current_app.config["APP_NAME"],
        reset_url=urljoin(url_for("admin.catch_all", _external=True), "auth/reset_password/" + token),
    )


def send_registration_confirmation_email(user):
    token = user.generate_confirmation_token(expiration=current_app.config["JWT_TOKEN_EXPIRATION_TIME"])
    send_email(
        user.email,
        "Confirm your account",
        "api/auth/email/confirm",
        user=user,
        token=token,
        confirmation_url=urljoin(url_for("admin.catch_all", _external=True), "auth/confirm/" + token),
    )
