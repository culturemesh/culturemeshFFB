"""
Contains forms for the top-level site.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email_or_username = StringField(
        'Email/Username', validators=[DataRequired()]
    )
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstname = StringField(
        'firstname', validators=[DataRequired()]
    )
    lastname = StringField(
        'lastname', validators=[DataRequired()]
    )
    username = StringField(
        'username', validators=[DataRequired()]
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    password = StringField('password', validators=[DataRequired()])
    confirm_password = StringField(
        'confirm_password', validators=[DataRequired()]
    )
    submit = SubmitField('Login')
