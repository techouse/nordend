from flask_babel import _, lazy_gettext as _l
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, Optional

from ..models import Role, User


class UserForm(FlaskForm):
    email = StringField(_l("E-mail"), validators=[InputRequired(), Email(), Length(min=1, max=120)])
    name = StringField(_l("Name"), validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField(_l("Password"), validators=[Optional(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Repeat Password"), validators=[Optional(), EqualTo("password")])
    location = StringField(_l("Location"), validators=[Length(min=0, max=64)])
    about_me = TextAreaField(_l("About me"))
    submit = SubmitField(_l("Submit"))

    def validate_email(self, field):
        if field.data != current_user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError(_l("Email already registered"))


class UserAdminCreateForm(FlaskForm):
    email = StringField(_l("E-mail"), validators=[InputRequired(), Email(), Length(min=1, max=120)])
    confirmed = BooleanField(_l("Confirmed"), validators=[InputRequired()])
    role = SelectField(_l("Role"), coerce=int, validators=[InputRequired()])
    name = StringField(_l("Name"), validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField(_l("Password"), validators=[InputRequired(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Repeat Password"), validators=[InputRequired(), EqualTo("password")])
    location = StringField(_l("Location"), validators=[Length(min=0, max=64)])
    about_me = TextAreaField(_l("About me"))
    submit = SubmitField(_l("Submit"))

    def __init__(self, *args, **kwargs):
        super(UserAdminCreateForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.id).all()]
        self.role.default = Role.query.filter_by(default=True).first().id

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l("Email already registered"))


class UserAdminForm(FlaskForm):
    email = StringField(_l("E-mail"), validators=[InputRequired(), Email(), Length(min=1, max=120)])
    confirmed = BooleanField(_l("Confirmed"))
    role = SelectField(_l("Role"), coerce=int)
    name = StringField(_l("Name"), validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField(_l("Password"), validators=[Optional(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Repeat Password"), validators=[Optional(), EqualTo("password")])
    location = StringField(_l("Location"), validators=[Length(min=0, max=64)])
    about_me = TextAreaField(_l("About me"))
    submit = SubmitField(_l("Submit"))

    def __init__(self, user, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.id).all()]
        self.role.default = Role.query.filter_by(default=True).first().id
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError(_l("Email already registered"))


class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=255)])
    body = CKEditorField("Content", validators=[InputRequired()])
    submit = SubmitField("Submit")
