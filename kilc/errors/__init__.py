from flask import Blueprint

bp = Blueprint('errors', __name__)

from kilc.errors import handlers