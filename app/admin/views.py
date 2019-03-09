from flask import render_template, flash, redirect, url_for, request, g, abort
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from app.decorators import admin_required, permission_required
from .forms import PostForm, UserAdminForm, UserForm
from .. import db
from . import admin
from ..models import User, Post, Permission, Role


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


@admin.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = UserForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if form.password.data:
            current_user.password = form.password.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(_("Your profile was successfully updated!"))
        return redirect(url_for(".edit_profile"))
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("admin/profile.html", form=form)


@admin.route("/users/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def user(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    form = UserAdminForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        if form.password.data:
            current_user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash(_("User was successfully updated!"))
        return redirect(url_for(".user", id=user.id))
    form.name.data = user.name
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template("admin/user.html", form=form, user=user)


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
