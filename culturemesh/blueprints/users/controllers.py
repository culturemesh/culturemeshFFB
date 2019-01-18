from flask import Blueprint, render_template
from culturemesh.client import Client

import flask_login
import http.client as httplib

from culturemesh.utils import get_network_title
from culturemesh.utils import get_user_image_url
from culturemesh.utils import get_short_network_join_date
from culturemesh.utils import get_time_ago

from culturemesh.blueprints.users.config import MAX_NETWORKS_TO_LOAD


users = Blueprint('users', __name__, template_folder='templates')

@users.route('/<int:user_id>/', methods=['GET'])
def user_profile(user_id):

  c = Client(mock=False)

  user = c.get_user(user_id)
  user['img_url'] = get_user_image_url(user)
  user_networks = c.get_user_networks(user_id, MAX_NETWORKS_TO_LOAD)

  networks = []
  for network in user_networks:
    network_ = {'id': network['id']}
    network_['title'] = get_network_title(network)
    network_['join_date'] = get_short_network_join_date(network)
    num_users = c.get_network_user_count(network['id'])['user_count']
    network_['user_count'] = num_users
    networks.append(network_)

  return render_template('profile.html', user=user, networks=networks)
