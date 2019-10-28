from flask import Blueprint, render_template, request, redirect, url_for, abort, Flask
from culturemesh.client import Client
from culturemesh import mail
from flask_login import current_user
from flask_login import login_required
from flask_mail import Message, Mail
import os
import datetime

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
        formdata = request.form
        feedback = formdata['feedback']
        user_info = 'guest user'
        if current_user.get_id() != None:
            user_info = current_user.get_id()


        msg = Message(str(datetime.datetime.now()),
                      sender = 'culturemesh.feedback@gmail.com',
                      recipients = ['culturemesh.feedback@gmail.com'], )
        msg.body = user_info + ':\n\n' + feedback
        mail.send(msg)
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
