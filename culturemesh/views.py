"""
Contains the views and templates for the top-level site. This includes:
  - The home page
  - The about page
  - The registration page
  - The login page
"""
import http.client as httplib
import requests
import config
import flask_login
import werkzeug
import json

from flask_wtf.csrf import CSRFError
from flask import render_template, request, redirect, session, abort
from culturemesh import app, login_manager
from culturemesh.client import Client
from flask_login import current_user
from culturemesh.forms import LoginForm, RegisterForm
from culturemesh.models import User
from culturemesh.constants import LOGIN_MSG, LOGIN_FAILED_MSG, LOGIN_ERROR
from culturemesh.constants import REGISTER_MSG, \
  REGISTER_PASSWORDS_DONT_MATCH_MSG, REGISTER_ERROR_MSG, \
  REGISTER_USERNAME_TAKEN_MSG, REGISTER_EMAIL_TAKEN_MSG, PRIVACY_MSG, \
  REGISTER_UPSTREAM_ERROR_MSG

from culturemesh.utils import email_registered, username_taken

@app.route("/")
@app.route("/index/")
def home():
	return render_template('index.html',  msg=LOGIN_MSG, form=LoginForm())

@app.route("/about/")
def about():
	return render_template('about.html')

# @app.route("/search/")
# def search():
#     return render_template('')

@app.route("/aboutIndexPage/")
def aboutIndexPage():
    return render_template('aboutIndexPage.html')

@app.route("/register/", methods=['GET', 'POST'])
def register():
  if current_user and current_user.is_authenticated:
     return redirect(url_for('home'))

  def make_register_page_tmpl(message, data_=None):
      return render_template(
        'register.html',
        msg=message,
        privacy_msg=PRIVACY_MSG,
        form=RegisterForm(data=data_)
      )

  if request.method == 'POST':
    form = RegisterForm(request.form)

    firstname = request.form['firstname'].strip()
    lastname = request.form['lastname'].strip()
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    confirm_password = request.form["confirm_password"].strip()

    data = {
      'firstname': firstname,
      'lastname': lastname,
      'username': username,
      'email': email,
      'password': '',
      'confirm_password': ''
    }

    if not form.validate():
      return make_register_page_tmpl(REGISTER_ERROR_MSG, data)

    c = Client(mock=False)

    if password != confirm_password:
      return make_register_page_tmpl(REGISTER_PASSWORDS_DONT_MATCH_MSG, data)

    user = {
      'username': username,
      'password': password,
      'first_name': firstname,
      'last_name': lastname,
      'email': email,
      'role': '0',
      'about_me': '',
      'gender': '',
      'act_code': 'NULL' # TODO: what to do here?
    }

    try:
      c.create_user(user)
    except werkzeug.exceptions.BadRequest:
      return make_register_page_tmpl(REGISTER_UPSTREAM_ERROR_MSG, data)

    return attempt_login(c, username, password)

  else:
    return make_register_page_tmpl(REGISTER_MSG)

@app.route("/login/", methods=['GET', 'POST'])
def render_login_page():
    if request.method == 'POST':
      if not LoginForm(request.form).validate():
        return render_template(
          'login.html', msg=LOGIN_ERROR, form=LoginForm()
        )

      email_or_username = request.form['email_or_username']
      password = request.form['password']
      return attempt_login(Client(mock=False), email_or_username, password)
    else:
        return render_template('login.html', msg=LOGIN_MSG, form=LoginForm())

@app.errorhandler(httplib.UNAUTHORIZED)
@app.route("/logout/")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/index/')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/index/')


##################### Other functions #########################

@app.after_request
def add_custom_http_response_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=86400; includeSubDomains"
    response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https://www.culturemesh.com;"
    response.headers["X-CultureMesh"] = "lite"
    return response

def attempt_login(c, email_or_username, password):
  """Attempts to login a user from an email/username and password combo.

  If successful: initiates a user session and redirects to home.
  If unsucessful: Returns the login page with the 'unauthorized' message.
  """
  try:
    token = c.get_token(email_or_username, password)
  except werkzeug.exceptions.Unauthorized as ex:
    # Unauthorized.
    return render_template(
      'login.html', msg=LOGIN_FAILED_MSG, form=LoginForm()
    )

  user_dict = c.get_user(token['id'])
  user = User(user_dict, api_token=token)
  flask_login.login_user(user)
  return redirect('/home/')

@login_manager.user_loader
def load_user(user_json_str):
  try:
    return User(json.loads(user_json_str))
  except Exception:
    abort(httplib.INTERNAL_SERVER_ERROR)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(CSRFError)
@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
@app.errorhandler(httplib.METHOD_NOT_ALLOWED)
def internal_server_error(e):
    return render_template('error.html')
