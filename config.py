import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    APP_NAME = os.environ.get('APP_NAME') or 'Flask'
    DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE') or 'en'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'im-not-lazy-im-just-very-relaxed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
