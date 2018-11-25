from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError, Length

from kilc.models import User


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(max=64)])
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different e-mail address'))


class EditProfileForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired(), Length(max=64)])
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email(), Length(max=120)])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=255)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(_('Please chose a different e-mail address'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('E-mail'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
