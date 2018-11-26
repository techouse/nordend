from flask import render_template, flash, redirect, url_for, request, g
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from .. import db
from ..main import main
from ..main.forms import EditProfileForm
from ..models import User


@main.before_app_request
def before_request():
    g.locale = str(get_locale())


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title=_('Home Page'))


@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@main.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.avatar_hash = current_user.gravatar_hash()
        db.session.commit()
        flash(_('Your changes have been saved'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)
