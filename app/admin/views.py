from flask import render_template, flash, redirect, url_for, request, g, abort, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from app.decorators import admin_required, permission_required
from .forms import PostForm, UserAdminForm, UserForm, UserAdminCreateForm
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


@admin.route("/profile", methods=["GET", "POST", "PUT"])
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
    return render_template("admin/users/profile.html", form=form)


@admin.route("/users")
@login_required
@admin_required
def users_index():
    page = request.args.get("page", 1, type=int)
    pagination = User.query.order_by(User.id.asc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    users = pagination.items
    return render_template("admin/users/index.html", users=users, pagination=pagination)


@admin.route("/users/create", methods=["GET", "POST"])
@login_required
@admin_required
def users_create():
    form = UserAdminCreateForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            confirmed=form.confirmed.data,
            role=Role.query.get(form.role.data),
            location=form.location.data,
            about_me=form.about_me.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash(_("User was successfully created!"))
        return redirect(url_for(".user", id=user.id))
    return render_template("admin/users/create.html", form=form)


@admin.route("/users/<int:id>", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
@admin_required
def user(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    form = UserAdminForm(user=user)
    if form.is_submitted():
        if request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
        elif form.validate_on_submit():
            user.name = form.name.data
            user.email = form.email.data
            user.confirmed = form.confirmed.data
            user.role = Role.query.get(form.role.data)
            user.location = form.location.data
            user.about_me = form.about_me.data
            if form.password.data:
                user.password = form.password.data
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
    return render_template("admin/users/edit.html", form=form, user=user)


@admin.route("/pages")
@login_required
@admin_required
def pages_index():
    return render_template("admin/pages.html", title="Pages")


@admin.route("/posts")
@login_required
@permission_required(Permission.WRITE)
def posts_index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    return render_template("admin/posts/index.html", posts=posts, pagination=pagination)


@admin.route("/posts/create", methods=["GET", "POST"])
@login_required
@permission_required(Permission.WRITE)
def posts_create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".post", id=post.id))
    return render_template("admin/posts/create.html", form=form)


@admin.route("/posts/<int:id>", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
@permission_required(Permission.WRITE)
def post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    form = PostForm()
    if form.is_submitted():
        if request.method == "DELETE":
            db.session.delete(post)
            db.session.commit()
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.session.add(post)
            db.session.commit()
            flash(_("Post was successfully updated!"))
            return redirect(url_for(".post", id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template("admin/posts/edit.html", form=form, post=post)
