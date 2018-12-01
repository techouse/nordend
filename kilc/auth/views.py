from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from .. import db
from ..auth import auth
from ..auth.email import send_password_reset_email
from ..auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from ..email import send_email
from ..models import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if (
            not current_user.confirmed
            and request.endpoint
            and request.blueprint != "auth"
            and request.endpoint != "static"
        ):
            return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title=_("Sign In"), form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.admin"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, _("Confirm your account"), "auth/email/confirm", user=user, token=token)
        flash(_("A confirmation email has been sent to you by email."))
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", title=_("Register"), form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash(_("You have confirmed your account. Thanks!"))
    else:
        flash(_("The confirmation link is invalid or has expired."))
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, _("Confirm Your Account"), "auth/email/confirm", user=current_user, token=token)
    flash(_("A new confirmation email has been sent to you by email."))
    return redirect(url_for("main.index"))


@auth.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", title=_("Reset Password"), form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash(_("Your password has been reset"))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
