from flask import Blueprint

bp = Blueprint('auth', __name__)

from kilc.auth import routes