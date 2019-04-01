from flask import render_template, g
from flask_babel import _, get_locale

from . import main


@main.before_app_request
def before_request():
    g.locale = str(get_locale())


@main.route("/")
@main.route("/index")
def index():
    return render_template("index.html", title=_("Home Page"))
