import os

from dotenv import load_dotenv
from str2bool import str2bool

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    # Website settings
    APP_NAME = os.environ.get("APP_NAME") or "Flask"
    LANGUAGES = ["en", "de", "it", "sl"]
    # Security settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "im-not-lazy-im-just-very-relaxed"
    WTF_CSRF_TIME_LIMIT = int(os.environ.get("WTF_CSRF_TIME_LIMIT")) or 3600
    JWT_TOKEN_EXPIRATION_TIME = int(os.environ.get("JWT_TOKEN_EXPIRATION_TIME")) or 3600
    PUBLIC_REGISTRATION_ENABLED = str2bool(os.environ.get("PUBLIC_REGISTRATION_ENABLED")) or False
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email server settings
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = os.environ.get("MAIL_SUBJECT_PREFIX") or APP_NAME
    MAIL_SENDER = os.environ.get("MAIL_SUBJECT_PREFIX") or "your-email@example.com"
    ADMINS = list(os.environ.get("ADMINS").split())
    # Pagination
    POSTS_PER_PAGE = int(os.environ.get("POSTS_PER_PAGE")) or 20
    PAGINATION_PAGE_ARGUMENT_NAME = os.environ.get("PAGINATION_PAGE_ARGUMENT_NAME") or "page"
    PAGINATION_PER_PAGE_ARGUMENT_NAME = os.environ.get("PAGINATION_PER_PAGE_ARGUMENT_NAME") or "per_page"
    # Images
    PUBLIC_IMAGE_PATH = "static/images/public/"
    MAX_IMAGE_CONTENT_LENGTH = int(os.environ.get("MAX_IMAGE_CONTENT_LENGTH")) or 2 * 1024 ** 2  # 2MB
    ALLOWED_IMAGE_EXTENSIONS = set(os.environ.get("ALLOWED_IMAGE_EXTENSIONS").lower().split()) or {"png", "jpg", "jpeg",
                                                                                                   "gif"}
    JPEG_COMPRESSION_QUALITY = int(os.environ.get("JPEG_COMPRESSION_QUALITY")) or 90
    IMAGE_SIZES = {220, 280, 440, 620, 920, 1920}
