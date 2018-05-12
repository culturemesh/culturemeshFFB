import flask_login
import utils

from flask import Blueprint, render_template
from culturemesh.client import Client
from flask_login import current_user

user_home = Blueprint('user_home', __name__, template_folder='templates')

@user_home.route("/")
@user_home.route("/dashboard")
@flask_login.login_required
def render_user_home():
  user_id = current_user.get_id()
  c = Client(mock=True)
  user = c.get_user(user_id)
  events_hosting = c.get_user_events(user_id, "hosting", 5)
  if user is None:
    return page_not_found("")

  for event in events_hosting:
    utils.enhance_event_date_info(event)

  return render_template('dashboard.html', user=user, events_hosting=events_hosting)

@user_home.route("/account")
@flask_login.login_required
def render_user_home_account():
  user_id = current_user.get_id()
  c = Client(mock=True)
  user = c.get_user(user_id)

  if user is None:
    return page_not_found("")
  return render_template('account.html', user=user)

@user_home.route("/events")
@flask_login.login_required
def render_user_home_events():
  user_id = current_user.get_id()
  c = Client(mock=True)
  user = c.get_user(user_id)

  if user is None:
    return page_not_found("")

  # TODO: incorporate paging into the events hosting API call
  events_hosting = c.get_user_events(user_id, "hosting", 5)
  if events_hosting is None:
    return page_not_found("")

  for event in events_hosting:
    utils.enhance_event_date_info(event)

  return render_template('events.html', user=user,
    events_hosting=events_hosting)

@user_home.route("/networks")
@flask_login.login_required
def render_user_home_networks():
  user_id = current_user.get_id()
  c = Client(mock=True)
  user = c.get_user(user_id)

  if user is None:
    return page_not_found("")

  # TODO: incorporate paging into the user networks call.
  user_networks = c.get_user_networks(user_id, count=5)
  # TODO: construct network titles

  networks = [] # TODO: make this a dedicated object.
  for network in user_networks:
    title_template = "From %s, %s, %s in %s, %s, %s, that speak %s."
    location_cur = network['location_cur']
    city = c.get_city(location_cur['city_id'])['name']
    region = c.get_region(location_cur['region_id'])['name']
    country = c.get_country(location_cur['country_id'])['name']

    location_origin = network['location_origin']
    city_orig = c.get_city(location_origin['city_id'])['name']
    region_orig = c.get_region(location_origin['region_id'])['name']
    country_orig = c.get_country(location_origin['country_id'])['name']

    network_ = {'title':'', 'id': network['id']}

    language = network['language_origin']['name']
    network_['title'] = title_template % (city_orig.title(), region_orig.title(), country_orig.title(),
                                    city.title(), region.title(), country.title(), language)
    networks.append(network_)

  return render_template('networks.html', user=user, networks=networks)
  
@user_home.route("/ping")
@flask_login.login_required
def ping():
  c = Client()
  return c.ping_user()
