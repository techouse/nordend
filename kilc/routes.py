from flask import render_template, flash, redirect, url_for

from kilc import app
from kilc.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    context = {'user': {'name': 'Klemen'}}

    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
