from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class FeedbackForm(FlaskForm):
    feedback = TextAreaField(
      'feedback', validators=[
        InputRequired(message="Please enter your feedback"),
      ],
      render_kw={'autofocus': True}
    )

    submit = SubmitField('Submit')
