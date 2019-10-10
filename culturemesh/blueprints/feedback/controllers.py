from flask import Blueprint, render_template, request, redirect, url_for, abort
from culturemesh.client import Client
from flask_login import current_user
from flask_login import login_required

from utils import enhance_event_date_info, parse_date

from culturemesh.blueprints.feedback.forms.feedback_forms import *

import http.client as httplib

feedback = Blueprint('feedback', __name__, template_folder='templates')

@feedback.route("/ping/")
@login_required
def ping():
  c = Client(mock=False)
  return c.ping_event()

@feedback.route("/", methods=['GET', 'POST'])
def render_feedback_form():
    if(request.method == 'POST'):
        feedback = request.form
        print("2")
        form_submitted = FeedbackForm(request.form)
        if(form_submitted.validate):
            #replace later
            feedback = feedback['feedback']
        print("hi")
        return redirect('/feedback/submitted/')

    return render_template(
      'feedback_form.html',
      feedback_form = FeedbackForm()
    )

@feedback.route("/submitted/")
def submitted():
  return render_template(
    'submitted.html'
    )
