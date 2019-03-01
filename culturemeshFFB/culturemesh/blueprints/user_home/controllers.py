import copy
import flask_login
import utils
import datetime

from flask import Blueprint, render_template, request
from flask_login import current_user
from werkzeug.exceptions import HTTPException
from utils import parse_date

from culturemesh.client import Client

from culturemesh.utils import get_network_title
from culturemesh.utils import get_user_image_url
from culturemesh.utils import get_short_network_join_date
from culturemesh.utils import get_time_ago

from culturemesh.utils import get_upcoming_events_by_user
from culturemesh.utils import get_upcoming_events_by_user_hosting
from culturemesh.utils import get_upcoming_events_by_user_attending

from culturemesh.blueprints.user_home.forms.home_forms import UserInfo
from culturemesh.blueprints.user_home.config import NUM_LATEST_POSTS_TO_DISPLAY
from culturemesh.blueprints.user_home.config import NUM_UPCOMING_EVENTS_TO_DISPLAY
from culturemesh.blueprints.user_home.config import NUM_EVENT_HOSTING_TO_DISPLAY
from culturemesh.blueprints.user_home.config import NUM_EVENT_ATTENDING_TO_DISPLAY
from culturemesh.blueprints.user_home.config import MAX_NETWORKS_TO_LOAD

user_home = Blueprint('user_home', __name__, template_folder='templates')

@user_home.route("/")
@user_home.route("/dashboard/")
@flask_login.login_required
def render_user_home():
  user = copy.deepcopy(current_user)

  c = Client(mock=False)
  user.img_url = get_user_image_url(user)

  # Events user is hosting
  events_hosting = get_upcoming_events_by_user_hosting(
    c, user.id, NUM_EVENT_HOSTING_TO_DISPLAY
  )
  # Events user is attending
  events_attending = get_upcoming_events_by_user_attending(
    c, user.id, NUM_EVENT_ATTENDING_TO_DISPLAY
  )

  # Upcoming events in user's networks.
  upcoming_events = get_upcoming_events_by_user(
    c, user.id, NUM_UPCOMING_EVENTS_TO_DISPLAY
  )

  # Some latest posts in the user's networks.
  latest_posts = c.get_user_posts(user.id, NUM_LATEST_POSTS_TO_DISPLAY)
  for post in latest_posts:
    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

    try:
      post['network'] = c.get_network(post['id_network'])
      post['network_title'] = get_network_title(post['network'])
    except HTTPException as e:
      post['network'] = None
      post['network_title'] = "Unknown"


  return render_template(
    'dashboard.html',
    user=user.as_dict,
    events_hosting=events_hosting,
    events_attending=events_attending,
    latest_posts=latest_posts,
    upcoming_events_in_networks=upcoming_events
  )

@user_home.route("/account/")
@flask_login.login_required
def render_user_home_account():
  user = copy.deepcopy(current_user)
  c = Client(mock=False)
  user.img_url = get_user_image_url(user)

  if user is None:
    return page_not_found("")

  user_info_form=UserInfo()
  user_info_form.first_name.process_data(user.first_name)
  user_info_form.last_name.process_data(user.last_name)
  user.about_me = user.about_me if user.about_me and user.about_me != "None" else ""
  user_info_form.about_me.process_data(user.about_me)
  return render_template(
    'account.html', user=user.as_dict, user_info_form=user_info_form
  )

@user_home.route("/update_profile/", methods=['POST'])
@flask_login.login_required
def update_profile_and_render_home():
  user_id = current_user.id
  c = Client(mock=False)

  data = request.form
  form = UserInfo(request.form)
  first_name = data['first_name']
  last_name = data['last_name']
  about_me = data['about_me']
  if not about_me:
    about_me = ""

  user = {
    'id': user_id, 'first_name': first_name,
    'last_name': last_name, 'about_me': about_me
  }

  if form.validate():
    c.update_user(current_user, user)

  user = c.get_user(user_id)
  if user is None:
    return page_not_found("")
  user['img_url'] = get_user_image_url(current_user)
  user_info_form = UserInfo()
  user_info_form.first_name.process_data(user['first_name'])
  user_info_form.last_name.process_data(user['last_name'])
  user_info_form.about_me.process_data(user['about_me'])
  return render_template(
    'account.html', user=user, user_info_form=user_info_form
  )

@user_home.route("/events/")
@flask_login.login_required
def render_user_home_events():
  c = Client(mock=False)
  user = copy.deepcopy(current_user)
  user_id = user.id
  user.img_url = get_user_image_url(user)

  # Events user is hosting
  events_hosting = get_upcoming_events_by_user_hosting(
    c, user.id, 50
  )
  # Events user is attending
  events_attending = get_upcoming_events_by_user_attending(
    c, user.id, 50
  )

  return render_template(
    'events.html',
    user=user.as_dict,
    events_hosting=events_hosting,
    events_attending=events_attending
  )

@user_home.route("/networks/")
@flask_login.login_required
def render_user_home_networks():
  c = Client(mock=False)
  user = copy.deepcopy(current_user)
  user_id = user.id
  user.img_url = get_user_image_url(user)

  if user is None:
    return page_not_found("")

  user_networks = c.get_user_networks(
    user_id, count=MAX_NETWORKS_TO_LOAD
  )

  networks = []
  for network in user_networks:
    network_ = {'id': network['id']}
    network_['title'] = get_network_title(network)
    network_['join_date'] = get_short_network_join_date(network)
    num_users = c.get_network_user_count(network['id'])['user_count']
    network_['user_count'] = num_users
    networks.append(network_)

  return render_template('networks.html', user=user.as_dict, networks=networks)

@user_home.route("/ping/")
@flask_login.login_required
def ping():
  c = Client(mock=False)
  return c.ping_user()
