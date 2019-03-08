from flask import render_template, flash, redirect, url_for, request, g
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from app.decorators import admin_required, permission_required
from .forms import PostForm
from .. import db
from . import admin
from ..models import User, Post, Permission


@admin.before_app_request
def before_request():
    g.locale = str(get_locale())


@admin.route("/")
@login_required
@permission_required(Permission.WRITE)
def index():
    return render_template("admin/index.html", title="Administration")


@admin.route("/users")
@login_required
@admin_required
def users():
    return render_template("admin/users.html", title="Users")


@admin.route("/pages")
@login_required
@admin_required
def pages():
    return render_template("admin/pages.html", title="Pages")


@admin.route("/posts")
@login_required
@permission_required(Permission.WRITE)
def posts():
    # form = PostForm()
    # if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
    #     post = Post(body=form.body.data,
    #                 author=current_user._get_current_object())
    #     db.session.add(post)
    #     db.session.commit()
    #     return redirect(url_for("admin.posts"))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("admin/posts.html", title="Posts", posts=posts)
