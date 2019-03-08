from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, InputRequired, EqualTo, ValidationError, Length

from ..models import User


class LoginForm(FlaskForm):
    email = StringField(_l("Email"), validators=[InputRequired(), Email(), Length(min=0, max=120)])
    password = PasswordField(_l("Password"), validators=[InputRequired(), Length(min=8, max=128)])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class RegistrationForm(FlaskForm):
    name = StringField(_l("Name"), validators=[InputRequired(), Length(min=0, max=64)])
    email = StringField(_l("E-mail"), validators=[InputRequired(), Email(), Length(min=0, max=120)])
    password = PasswordField(_l("Password"), validators=[InputRequired(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Repeat Password"), validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField(_l("Register"))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_("Please use a different e-mail address"))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("E-mail"), validators=[InputRequired(), Email()])
    submit = SubmitField(_l("Request Password Reset"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[InputRequired(), Length(min=8)])
    password2 = PasswordField(_l("Repeat Password"), validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField(_l("Request Password Reset"))
