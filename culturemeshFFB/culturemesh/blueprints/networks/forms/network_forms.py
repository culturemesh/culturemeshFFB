from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class NetworkJoinForm(FlaskForm):
    submit = SubmitField('Join Network')

class NetworkLeaveForm(FlaskForm):
    submit = SubmitField('Yes, Leave Network')

class CreatePostForm(FlaskForm):
    post_content = StringField(
      'post_content', validators=[
        InputRequired(message="Post cannot be empty."),
      ],
      widget=TextArea(),
      render_kw={'autofocus': True}
    )
    submit = SubmitField('Create Post')

class CreateEventForm(FlaskForm):
    title = StringField(
      'title', validators=[
        InputRequired(message="Event title cannot be empty."),
      ],
      render_kw={'autofocus': True}
    )

    country = StringField(
      'country', validators=[
        InputRequired(message="You must specify the country of the even."),
      ]
    )

    region = StringField(
      'region'
    )

    city = StringField(
      'city'
    )

    address_1 = StringField(
      'address_1', validators=[
        InputRequired(message="You must supply an address field."),
      ]
    )

    address_2 = StringField(
      'address_2',
    )

    event_date = DateTimeField(
      'event_date', validators=[
        InputRequired(message="You must specify the date of the event."),
      ]
    )

    description = StringField(
      'description', validators=[
        InputRequired(message="Description cannot be empty."),
      ],
      widget=TextArea()
    )

    submit = SubmitField('Create Event')


