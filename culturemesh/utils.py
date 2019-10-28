"""
Contains utilities used by more than one blueprint.
Otherwise, utilities are found in a dedicated utils file within
that blueprint.
"""

import pytz

from flask import abort

from culturemesh.constants import BLANK_PROFILE_IMG_URL
from culturemesh.constants import USER_IMG_URL_FMT
from culturemesh.client import Client
from datetime import datetime, timezone

from utils import parse_date
from utils import get_month_abbr
from utils import enhance_event_date_info

import http.client as httplib

utc=pytz.UTC

def safe_get_query_arg(request, arg_name):
  arg = request.args.get(arg_name)
  if not arg:
    abort(httplib.NOT_FOUND)
  return arg

def username_taken(client, username):
  """True if the username is already taken
  """
  return False

def email_registered(client, email):
  """True if email is registered with an account already.
  """
  return False

def get_network_title(network):
  """Returns the title of a network given a network
  JSON as a dict
  """

  cur_country = network['country_cur']
  cur_region = network['region_cur']
  cur_city = network['city_cur']

  orig_country = network['country_origin']
  orig_region = network['region_origin']
  orig_city = network['city_origin']

  cur_location = ', '.join(
    [l for l in [cur_city, cur_region, cur_country] if l]
  )

  orig_location = ', '.join(
    [l for l in [orig_city, orig_region, orig_country] if l]
  )

  if network['network_class'] == '_l':

    # Language network
    language = network['language_origin']
    return "%s speakers in %s" % (language, cur_location)

  elif network['network_class'] == 'cc' \
    or network['network_class'] == 'rc' \
    or network['network_class'] == 'co':

    # City network (cc), region network (rc), or
    # country network (co).
    # Title-wise, we treat them all the same.

    return 'From %s in %s' % (orig_location, cur_location)

  else:
    return "Unknown"

def populate_network_with_location_names(client, network):
  for location in ['location_origin', 'location_cur']:
    network[location]['city_name'] = client.get_city(
        network[location]['city_id']
    )['name']
    network[location]['country_name'] = client.get_country(
        network[location]['country_id']
    )['name']
    network[location]['region_name'] = client.get_region(
        network[location]['region_id']
    )['name']

def get_event_location(event):
  """Returns a string for where this event
  is taking place (i.e. New York City, New York).

  This does not return the address of an event, but
  its location.
  """
  city = event['city']
  region = event['region']
  country = event['country']

  location = ', '.join([l for l \
    in [city, region, country] if l])

  return location


def get_user_image_url(user):
  """Returns the URL of a user's profile image
  given a User object.
  """

  if type(user) == dict:
    if not user['img_link'] or user['img_link'] == "None":
      return BLANK_PROFILE_IMG_URL
    else:
      return USER_IMG_URL_FMT % user['img_link']
  else:
    if not user.img_link or user.img_link == "None":
      return BLANK_PROFILE_IMG_URL
    else:
      return USER_IMG_URL_FMT % user.img_link

def get_short_network_join_date(network):
  """Returns a short version of the user's Join
  date to a network:

  Mon day, Year
  """

  if 'join_date' not in network:
    return "unknown"
  else:
    date = parse_date(network['join_date'])
    short_month = get_month_abbr(date)
    year = date.year
    day = date.day
    return "%s %s, %s" % (str(short_month), str(day), str(year))

def get_time_ago(past_time):
  """Get a datetime object or a int() Epoch timestamp and return a
  pretty string like 'an hour ago', 'Yesterday', '3 months ago',
  'just now', etc

  Thanks: Stack Overflow id 1551382
  """

  now = datetime.now(timezone.utc)
  if type(past_time) is int:
    diff = now - datetime.fromtimestamp(past_time)
  elif isinstance(past_time, datetime):
    diff = now - past_time
  elif not past_time:
    diff = now - now
  elif isinstance(past_time, str):
    past_time = parse_date(past_time)
    diff = now - past_time
  else:
    return "unknown time ago"

  second_diff = diff.seconds
  day_diff = diff.days

  if day_diff < 0:
    return ''

  if day_diff == 0:
    if second_diff < 10:
      return "just now"
    if second_diff < 60:
      if int(second_diff) == 1:
        return str(second_diff) + " second ago"
      else:
        return str(second_diff) + " seconds ago"
    if second_diff < 120:
      return "a minute ago"
    if second_diff < 3600:
      minutes = round(second_diff / 60)
      if int(minutes) == 1:
        return str(minutes) + " minute ago"
      else:
        return str(minutes) + " minutes ago"
    if second_diff < 7200:
      return "an hour ago"
    if second_diff < 86400:
      hours = round(second_diff / 3600)
      if int(hours) == 1:
        return str(hours) + " hour ago"
      else:
        return str(hours) + " hours ago"
  if day_diff == 1:
    return "Yesterday"
  if day_diff < 7:
    if int(day_diff) == 1:
      return str(day_diff) + " day ago"
    else:
      return str(day_diff) + " days ago"
  if day_diff < 31:
    weeks = round(day_diff / 7)
    if int(weeks) == 1:
      return str(weeks) + " week ago"
    else:
      return str(weeks) + " weeks ago"

  if day_diff < 365:
    months = round(day_diff /30)
    if int(months) == 1:
      return str(round(day_diff /30)) + " month ago"
    else:
      return str(round(day_diff /30)) + " months ago"

  years = round(day_diff / 365)
  if int(years) == 1:
    return str(years) + " year ago"
  else:
    return str(years) + " years ago"


############### EVENTS ################

def enhance_event_info(client, events):
    for event in events:
        enhance_event_date_info(event)
        event['network_title'] = get_network_title(
          client.get_network(event['id_network'])
        )
        event['num_registered'] = client.get_event_reg_count(
          event['id']
        )['reg_count']
    return events

def trim_and_sort_events(events):
  """Sorts given events by event date, and
  trims those that are past today.
  """
  events = [
      e for e in events \
        if parse_date(e['event_date']) \
          >= utc.localize(datetime.now())
    ]

  events = sorted(
    events, key=lambda x: parse_date(x['event_date'])
  )
  return events

def get_upcoming_events_by_user(client, user_id, count):
  """Return up to 'count' events that are in the user's
  networks and which are upcoming, sorted by how close they
  are to today
  """
  upcoming_events = []
  networks = client.get_user_networks(user_id, 200)
  for network in networks:
    events = client.get_network_events(network['id'], 10)
    upcoming_events += events

  upcoming_events = trim_and_sort_events(upcoming_events)

  return enhance_event_info(
    client, upcoming_events[:min(len(upcoming_events), count)]
  )

def get_upcoming_events_by_user_hosting(client, user_id, count):
  """Return up to 'count' events that a user is hosting
  in the future, sorted by how close they
  are to today
  """
  upcoming_events = client.get_user_events_hosting(user_id, 50)
  upcoming_events = trim_and_sort_events(upcoming_events)
  return enhance_event_info(
    client, upcoming_events[:min(len(upcoming_events), count)]
  )


def get_upcoming_events_by_user_attending(client, user_id, count):
  """Return up to 'count' events that a user is attending
  in the future, sorted by how close they
  are to today
  """
  upcoming_events = client.get_user_events_attending(user_id, 50)
  upcoming_events = trim_and_sort_events(upcoming_events)
  return enhance_event_info(
    client, upcoming_events[:min(len(upcoming_events), count)]
  )

def get_upcoming_events_by_network(client, network_id, count):
  """Return up to 'count' events that are in a
  network and which are upcoming, sorted by how close they
  are to today"""
  upcoming_events = client.get_network_events(network_id, 50)
  upcoming_events = trim_and_sort_events(upcoming_events)
  return enhance_event_info(
    client, upcoming_events[:min(len(upcoming_events), count)]
  )

def user_is_attending_event(client, user_id, event):
  """Returns true if the given user is attending the given event
  object. Assumes no more than 500 people are registered for an event.
  """
  event_registration_list = client.get_event_registration_list(event['id'], 500)
  print(event_registration_list)
  for reg in event_registration_list:
      if reg['id_guest'] == int(user_id):
          return True
  return False

def is_logged_in(current_user):
    return current_user.get_id() != None
