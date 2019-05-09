import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import eventlet
eventlet.monkey_patch()

from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_cachebuster import CacheBuster
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config, basedir

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "admin.catch_all"
login.login_message = _l("Please login to access this page.")
mail = Mail()
babel = Babel()
cache_buster = CacheBuster(config={"extensions": [".js", ".css"], "hash_size": 10})
socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    cache_buster.init_app(app)

    from .errors import errors

    app.register_blueprint(errors)

    from .admin import admin

    app.register_blueprint(admin, url_prefix="/admin/")

    from .main import main

    app.register_blueprint(main)

    from .api import api_bp
    
    csrf.exempt(api_bp)
    app.register_blueprint(api_bp)

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"],
                subject=app.config["APP_NAME"] + " Error",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists(os.path.join(basedir, "logs")):
            os.mkdir(os.path.join(basedir, "logs"))
        file_handler = RotatingFileHandler(
            os.path.join(basedir, "logs", app.config["APP_NAME"] + ".log"), maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]")
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(app.config["APP_NAME"] + " startup")

    socketio.init_app(app)
    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])


from . import models
