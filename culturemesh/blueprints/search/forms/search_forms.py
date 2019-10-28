from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_type = SelectField(
        'Search Type',
        choices=[('location', 'are from'), ('language', 'speak')]
    )
    origin_or_language = StringField(
        'origin/language', validators=[DataRequired()]
    )
    residence = StringField(
        'current_location', validators=[DataRequired()]
    )
    submit = SubmitField('Search')

# Keep this form here so we can do CSRF protection.
class GoToNetworkForm(FlaskForm):
    pass
