from flask import render_template, flash, redirect, url_for, request, g
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from .. import db
from . import admin
from ..models import User


@admin.before_app_request
def before_request():
    g.locale = str(get_locale())


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')
