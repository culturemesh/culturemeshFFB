from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class UserInfo(FlaskForm):
    first_name = StringField(
      'first_name', validators=[
        InputRequired(message="First name cannot be empty."),
      ],
      render_kw={'autofocus': True}
    )
    last_name = StringField(
      'last_name', validators=[
        InputRequired(message="Last name cannot be empty.")
      ]
    )
    about_me = StringField('about_me', widget=TextArea())
    submit = SubmitField('Update')
