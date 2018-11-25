from flask import Blueprint

bp = Blueprint('main', __name__)

from kilc.main import routes