from flask import Blueprint, render_template, request, redirect, url_for, abort
from culturemesh.client import Client
from flask_login import current_user
from flask_login import login_required

from utils import enhance_event_date_info, parse_date

from culturemesh.utils import user_is_attending_event
from culturemesh.utils import get_network_title
from culturemesh.utils import get_event_location
from culturemesh.utils import safe_get_query_arg
from culturemesh.utils import is_logged_in

from culturemesh.blueprints.events.forms.event_forms import *
from culturemesh.blueprints.networks.utils import gather_network_info

import http.client as httplib

events = Blueprint('events', __name__, template_folder='templates')

@events.route("/ping/")
@login_required
def ping():
  c = Client(mock=False)
  return c.ping_event()

@events.route("/")
def render_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)
    date_info = {}
    enhance_event_date_info(event)
    event['num_registered'] = c.get_event_reg_count(event['id'])['reg_count']

    network = c.get_network(event['id_network'])
    event['network_title'] = get_network_title(network)
    event['location'] = get_event_location(event)
    host = c.get_user(event['id_host'])

    role = None

    if is_logged_in(current_user):
        user_id = current_user.id
        if event['id_host'] == int(user_id):

          # The current user is hosting this event.
          role = 'hosting'
          host['username'] = 'you'

        elif user_is_attending_event(c, user_id, event):

          # The current user is already signed up for this event.
          role = 'attending'
        else:

          # The current user is not signed up for this event.
          pass
    else:
        user_id = None

    return render_template(
      'event.html',
      event=event,
      host=host,
      role=role,
      curr_user_id=user_id,
      join_form=EventJoinForm(),
      leave_form=EventLeaveForm(),
      cancel_form=EventCancelForm()
    )

@events.route("/join/", methods=['POST'])
@login_required
def join_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    c.join_event_as_guest(current_user, current_event_id)
    return redirect(
      url_for('events.render_event', id=current_event_id)
    )

@events.route("/leave/", methods=['POST'])
@login_required
def leave_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    c.leave_event(current_user, current_event_id)
    return redirect(
      url_for('events.render_event', id=current_event_id)
    )

@events.route("/cancelconfirm/", methods=['POST'])
@login_required
def cancel_event_confirm():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)
    network = c.get_network(event['id_network'])
    network_info = gather_network_info(network['id'], current_user.id, c)

    # The current user should only be able to cancel an event if they
    # are the host of that event.
    if not str(current_user.id) == str(event['id_host']):
      return redirect(
        url_for('user_home')
      )

    return render_template(
      'event_cancel.html',
      network_info=network_info,
      event=event,
      form=EventCancelConfirmForm()
    )

@events.route("/cancel/", methods=['POST'])
@login_required
def cancel_event():
    current_event_id = request.args.get('id')
    c = Client(mock=False)
    event = c.get_event(current_event_id)

    # The current user should only be able to cancel an event if they
    # are the host of that event.
    if str(current_user.id) == str(event['id_host']):
      c.delete_event(current_user, current_event_id)
    return redirect(url_for('user_home.render_user_home'))


@events.route("/edit/", methods=["GET", "POST"])
@login_required
def edit_event():
  c = Client(mock=False)
  event_id = safe_get_query_arg(request, 'id')
  event = c.get_event(event_id)
  if event['id_host'] != current_user.id:
    abort(httplib.NOT_FOUND)

  edit_event_form = EditEventForm()

  event['network_title'] = get_network_title(
    c.get_network(event['id_network'])
  )

  edit_event_form.title.process_data(event['title'])
  edit_event_form.country.process_data(event['country'])
  edit_event_form.region.process_data(event['region'])
  edit_event_form.city.process_data(event['city'])
  edit_event_form.address_1.process_data(event['address_1'])
  edit_event_form.address_2.process_data(event['address_2'])
  edit_event_form.event_date.process_data(
    parse_date(event['event_date'])
  )
  edit_event_form.description.process_data(event['description'])

  error_msg = None

  if request.method == 'GET':
      pass
  else:
    data = request.form
    form_submitted = EditEventForm(request.form)
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
        'id': event_id,
        'title': title,
        'country': country,
        'region': region,
        'city': city,
        'address_1': address_1,
        'address_2': address_2,
        'event_date': event_date,
        'description': description
      }

      c.update_event(current_user, event)
      return redirect(
        url_for('events.render_event') + "?id=%s" % str(event_id)
      )
    else:
      error_msg = "Oops. An error occurred.  Did you enter all \
            of the form fields correctly?"

  return render_template(
    'edit_event.html',
    edit_event_form=edit_event_form,
    network_title=event['network_title'],
    current_user=current_user,
    curr_user_id=current_user.id,
    id_network=event['id_network'],
    error_msg=error_msg
  )
