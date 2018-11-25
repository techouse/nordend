from threading import Thread

from flask import render_template
from flask_babel import _
from flask_mail import Message

from kilc import app, mail


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_mail, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[%(app_name)s] Reset Your Password', app_name=app.config['APP_NAME']),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user,
                                         token=token,
                                         app_name=app.config['APP_NAME']),
               html_body=render_template('email/reset_password.html',
                                         user=user,
                                         token=token,
                                         app_name=app.config['APP_NAME']))
