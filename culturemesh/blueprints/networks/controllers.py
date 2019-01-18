import flask_login
import datetime
import utils
import pytz

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_network_title
from culturemesh.utils import get_upcoming_events_by_network
from culturemesh.utils import get_time_ago
from culturemesh.utils import is_logged_in
from utils import parse_date

from culturemesh.blueprints.networks.forms.network_forms import NetworkJoinForm
from culturemesh.blueprints.networks.forms.network_forms import CreatePostForm
from culturemesh.blueprints.networks.forms.network_forms import CreateEventForm
from culturemesh.blueprints.networks.forms.network_forms import NetworkLeaveForm

from culturemesh.blueprints.networks.utils import gather_network_info

networks = Blueprint('networks', __name__, template_folder='templates')
utc=pytz.UTC

@networks.route("/")
def network():
  id_network = request.args.get('id')
  c = Client(mock=False)

  id_user = current_user.get_id()
  network_info = gather_network_info(id_network, id_user, c)
  upcoming_events = get_upcoming_events_by_network(c, id_network, 3)

  return render_template(
    'network.html',
    network_info=network_info,
    form=NetworkJoinForm(),
    upcoming_events=upcoming_events
  )

@networks.route("/join/", methods=['POST'])
@flask_login.login_required
def join_network():
  id_network = request.args.get('id')
  id_user = current_user.id
  form = NetworkJoinForm(request.form)
  c = Client(mock=False)
  if form.validate():
    c.join_network(current_user, id_network)

  network_info = gather_network_info(id_network, id_user, c, "join")
  return render_template(
    'network.html', network_info=network_info, form=NetworkJoinForm()
  )

@networks.route("/events/")
def network_events() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  id_network = request.args.get('id')
  if not id_network :
    return render_template('404.html')
  c = Client(mock=False)
  try:
    id_network = int(id_network)
  except ValueError:
    return render_template('404.html')
  network = c.get_network(id_network)
  if not network:
    return render_template('404.html')

  events = None

  old_index = request.args.get('index')
  if not old_index:
    events = c.get_network_events(id_network, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    events = c.get_network_events(id_network, 10, old_index - 1)

  # TODO: Add better handling for when there's no posts left.

  if not events :
    event_index = old_index
  else :
    event_index = events[-1]['id']

  for event in events:
    utils.enhance_event_date_info(event)
    event['num_registered'] = c.get_event_reg_count(event['id'])['reg_count']

  user_is_member = False

  if is_logged_in(current_user):
      user_networks = c.get_user_networks(current_user.get_id(), count=100)
      for network_ in user_networks:
        if int(id_network) == int(network_['id']):
          user_is_member = True
          break

  network_info = {}
  network_info['id'] = id_network
  network_info['events'] = events
  network_info['network_title'] = get_network_title(network)
  network_info['user_is_member'] = user_is_member

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  referrer = request.headers.get("Referer")

  return render_template(
    'network_events.html', network_info=network_info,
    event_index=event_index, referer_url=referrer
  )

@networks.route("/posts/")
def network_posts() :
  # TODO: A lot of this code is repeated from network(), with just minor variations.
  # This should be factored out.
  id_network = request.args.get('id')
  if not id_network :
    return render_template('404.html')
  c = Client(mock=False)
  try:
    id_network = int(id_network)
  except ValueError:
    return render_template('404.html')

  network = c.get_network(id_network)
  if not network:
    return render_template('404.html')

  # TODO: Get user ID and work out if user is in network.
  # Add join us button to page if they're not.

  posts = None

  old_index = request.args.get('index')
  if not old_index:
    posts = c.get_network_posts(id_network, 10)
  else:
    try:
      old_index = int(old_index)
    except ValueError:
      return render_template('404.html')
    posts = c.get_network_posts(id_network, 10, old_index - 1)

  for post in posts:
    post['username'] = c.get_user(post['id_user'])['username']
    post['reply_count'] = c.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

  # TODO: Add better handling for when there's no events left.

  if not posts :
    post_index = old_index
  else :
    post_index = posts[-1]['id']

  user_is_member = False
  if is_logged_in(current_user):
      user_networks = c.get_user_networks(current_user.get_id(), count=100)
      for network_ in user_networks:
        if int(id_network) == int(network_['id']):
          user_is_member = True
          break

  network_info = {}
  network_info['id'] = id_network
  network_info['posts'] = posts
  network_info['user_is_member'] = user_is_member

  num_users = c.get_network_user_count(id_network)['user_count']
  num_posts = c.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts

  network_info['network_title'] = get_network_title(network)
  return render_template('network_posts.html', network_info=network_info, post_index=post_index)

@networks.route("/posts/new/", methods=['GET', 'POST'])
@flask_login.login_required
def create_new_post():
    c = Client(mock=False)
    id_network = request.args.get('id')
    user_id = current_user.id
    network = c.get_network(id_network)
    network_info = gather_network_info(id_network, user_id, c)

    if not network_info['user_is_member']:
      return render_template(
        'network_create_event_post_not_member.html',
        curr_user_id=user_id,
        id_network=id_network,
        network_info=network_info,
        form=NetworkJoinForm()
    )

    network_title = network_info['network_title']
    error_msg = None

    if request.method == 'GET':
      pass
    else:
      data = request.form
      form_submitted = CreatePostForm(request.form)
      if form_submitted.validate():
        post_text = data['post_content']

        post = {
          'id_user': user_id,
          'id_network': id_network,
          'post_text': post_text,
          'vid_link': "",
          'img_link': ""
        }

        c.create_post(current_user, post)
        return redirect(
          url_for('networks.network_posts') + "?id=%s" % str(id_network)
        )
      else:
        error_msg = "Oops. An error ocurred. Did you forget to add text to your \
          post before submitting?"

    new_form = CreatePostForm()

    return render_template(
      'network_create_post.html',
      curr_user_id=user_id,
      id_network=id_network,
      network_title=network_title,
      form=new_form,
      error_msg=error_msg
    )

@networks.route("/events/new/", methods=['GET', 'POST'])
@flask_login.login_required
def create_new_event():
    c = Client(mock=False)
    id_network = request.args.get('id')
    user_id = current_user.id
    network = c.get_network(id_network)
    network_info = gather_network_info(id_network, user_id, c)

    if not network_info['user_is_member']:
      return render_template(
        'network_create_event_post_not_member.html',
        curr_user_id=user_id,
        id_network=id_network,
        network_info=network_info,
        form=NetworkJoinForm()
    )

    network_title = network_info['network_title']
    error_msg = None

    if request.method == 'GET':
      pass
    else:
      data = request.form
      form_submitted = CreateEventForm(request.form)
      if form_submitted.validate():
        event_date = data['event_date']
        title = data['title']
        address_1 = data['address_1']
        address_2 = data.get('address_2', None)
        country = data['country']
        region = data.get('region', None)
        city = data.get('city', None)
        description = data['description']

        event = {
          "id_network": id_network,
          "id_host": user_id,
          "event_date": event_date,
          "title": title,
          "address_1": address_1,
          "address_2": address_2,
          "country": country,
          "region": region,
          "city": city,
          "description": description
        }

        c.create_event(current_user, event)
        return redirect(
          url_for('networks.network_events') + "?id=%s" % str(id_network)
        )
      else:
        error_msg = "Oops. An error occurred.  Did you enter all \
            of the form fields correctly?"

    new_form = CreateEventForm()
    return render_template(
      'network_create_event.html',
      curr_user_id=user_id,
      id_network=id_network,
      network_title=network_title,
      form=new_form,
      error_msg=error_msg
    )

@networks.route("/leave/", methods=['GET', 'POST'])
@flask_login.login_required
def leave():
    c = Client(mock=False)
    id_network = request.args.get('id')
    user_id = current_user.id
    network = c.get_network(id_network)
    network_info = gather_network_info(id_network, user_id, c)

    if request.method == 'GET':
      if not network_info['user_is_member']:
        return redirect(
          url_for('networks.network') + "?id=%s" % str(id_network)
        )
      return render_template(
        'network_leave.html',
        id_network=id_network,
        network_title=network_info['network_title'],
        form=NetworkLeaveForm()
      )
    elif request.method == 'POST':
      if network_info['user_is_member']:

        # NOTE: the two event deletion steps must happen in this order.
        #
        # Future TODO is to make this not a strict dependency.
        #

        # Delete all events this user is hosting in this network.
        events_hosting = c.get_user_events_hosting(
          user_id, 1000
        )
        for event in events_hosting:
          if str(event['id_network']) == str(network['id']):
            c.delete_event(current_user, str(event['id']))

        # Unregister from all events this user is attending in this network.
        events_attending = c.get_events_attending_in_network(
          current_user, network['id'], 1000
        )
        for event in events_attending:
          c.leave_event(current_user, event['id'])

        # Leave the network.
        c.leave_network(current_user, network['id'])

      return redirect(
          url_for('user_home.render_user_home_networks')
      )


@networks.route("/ping/")
@flask_login.login_required
def ping():
    c = Client(mock=False)
    return c.ping_network()
