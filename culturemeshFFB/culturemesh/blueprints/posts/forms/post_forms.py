from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class CreatePostReplyForm(FlaskForm):
    post_reply_content = StringField(
      'post_reply_content', validators=[
        InputRequired(message="Post reply cannot be empty."),
      ],
      widget=TextArea(),
      render_kw={'autofocus': True}
    )
    submit = SubmitField('Reply')

# Overloaded for posts and post replies.
class EditPostForm(FlaskForm):
    content = StringField(
      'content', validators=[
        InputRequired(message="Post cannot be empty."),
      ],
      widget=TextArea(),
      render_kw={'autofocus': True}
    )
    submit = SubmitField('Submit')
