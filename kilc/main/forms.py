from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, ValidationError, Length

from ..models import User


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
