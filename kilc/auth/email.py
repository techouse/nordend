from flask import current_app
from flask_babel import _

from ..email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(user.email,
               _('[%(app_name)s] Reset Your Password', app_name=current_app.config['APP_NAME']),
               'auth/email/reset_password',
               user=user,
               token=token,
               app_name=current_app.config['APP_NAME'])
