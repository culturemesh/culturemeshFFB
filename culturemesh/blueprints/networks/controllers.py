import flask_login
import utils

from flask import Blueprint, render_template, request
from culturemesh.client import Client

networks = Blueprint('networks', __name__, template_folder='templates')

@networks.route("/")
@flask_login.login_required
def network():
  network_id = request.args.get('id')
  if not network_id:
    return render_template('404.html')
  c = Client(mock=True)
  try:
    network_id = int(network_id)
  except ValueError:
    return render_template('404.html')
  network = c.get_network(network_id)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  posts = c.get_network_posts(network_id, 3)
  events = c.get_network_events(network_id, 3)
  for event in events:
    utils.enhance_event_date_info(event)

  for post in posts:
    post['username'] = c.get_user(post['user_id'])['username']

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['network_id'] = network_id
  network_info['posts'] = posts
  network_info['events'] = events
  cur_country = c.get_country(network['location_cur']['country_id'])
  cur_region = c.get_region(network['location_cur']['region_id'])
  cur_city = c.get_city(network['location_cur']['city_id'])

  if network['network_class'] == 0:
    language = network['language_origin']['name']
    network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title
  elif network['network_class'] == 1:
    orig_country = c.get_country(network['location_origin']['country_id'])
    orig_region = c.get_region(network['location_origin']['region_id'])
    orig_city = c.get_city(network['location_origin']['city_id'])
    network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title

  return render_template('network.html', network_info=network_info)

@networks.route("/events")
@flask_login.login_required
def network_events() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  network_id = request.args.get('id')
  if not network_id :
    return render_template('404.html')
  c = Client(mock=True)
  try:
    network_id = int(network_id)
  except ValueError:
    return render_template('404.html')
  network = c.get_network(network_id)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  events = None

  old_index = request.args.get('index')
  if not old_index:
    events = c.get_network_events(network_id, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    events = c.get_network_events(network_id, 10, old_index - 1)

  # TODO: Add better handling for when there's no posts left.

  if not events :
    event_index = old_index
  else :
    event_index = events[-1]['id']

  for event in events:
    utils.enhance_event_date_info(event)

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['network_id'] = network_id
  network_info['events'] = events
  cur_country = c.get_country(network['location_cur']['country_id'])
  cur_region = c.get_region(network['location_cur']['region_id'])
  cur_city = c.get_city(network['location_cur']['city_id'])

  if network['network_class'] == 0:
    language = network['language_origin']['name']
    network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title
  elif network['network_class'] == 1:
    orig_country = c.get_country(network['location_origin']['country_id'])
    orig_region = c.get_region(network['location_origin']['region_id'])
    orig_city = c.get_city(network['location_origin']['city_id'])
    network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title

  return render_template('network_events.html', network_info=network_info, event_index=event_index)

@networks.route("/posts")
@flask_login.login_required
def network_posts() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  network_id = request.args.get('id')
  if not network_id :
    return render_template('404.html')
  c = Client(mock=True)
  try:
    network_id = int(network_id)
  except ValueError:
    return render_template('404.html')
  network = c.get_network(network_id)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  posts = None

  old_index = request.args.get('index')
  if not old_index:
    posts = c.get_network_posts(network_id, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    posts = c.get_network_posts(network_id, 10, old_index - 1)

  posts = posts[::-1]
  for post in posts:
    post['username'] = c.get_user(post['user_id'])['username']

  # TODO: Add better handling for when there's no events left.

  if not posts :
    post_index = old_index
  else :
    post_index = posts[-1]['id']

  # TODO: This assumes that the region ID and city ID are specified in the data.
  # This is not necessarily the case. This needs to be changed using the new information
  # that Ian sent us about network classes.

  network_info = {}
  network_info['network_id'] = network_id
  network_info['posts'] = posts
  cur_country = c.get_country(network['location_cur']['country_id'])
  cur_region = c.get_region(network['location_cur']['region_id'])
  cur_city = c.get_city(network['location_cur']['city_id'])

  if network['network_class'] == 0:
    language = network['language_origin']['name']
    network_title = "%s speakers in %s, %s, %s" % tuple(map(lambda x: x.title(), [language, cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title
  elif network['network_class'] == 1:
    orig_country = c.get_country(network['location_origin']['country_id'])
    orig_region = c.get_region(network['location_origin']['region_id'])
    orig_city = c.get_city(network['location_origin']['city_id'])
    network_title = 'From %s, %s, %s in %s, %s, %s' % tuple(map(lambda x: x.title(), [orig_city['name'], orig_region['name'], orig_country['name'], cur_city['name'], cur_region['name'], cur_country['name']]))
    network_info['network_title'] = network_title

  return render_template('network_posts.html', network_info=network_info, post_index=post_index)

@networks.route("/ping")
@flask_login.login_required
def ping():
    c = Client()
    return c.ping_network()
