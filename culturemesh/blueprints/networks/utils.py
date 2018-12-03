"""Utilities for the networks module.
"""
import utils

from culturemesh.utils import get_network_title
from culturemesh.utils import get_time_ago

def gather_network_info(id_network, id_user, client, scenario="normal"):

  network = client.get_network(id_network)
  recent_posts = client.get_network_posts(id_network, 3)
  recent_events = client.get_network_events(id_network, 3)
  for event in recent_events:
    utils.enhance_event_date_info(event)

  for post in recent_posts:
    post['username'] = client.get_user(post['id_user'])['username']
    post['reply_count'] = client.get_post_reply_count(post['id'])['reply_count']
    post['time_ago'] = get_time_ago(post['post_date'])

  user_is_member = False
  if id_user is not None:
      user_networks = client.get_user_networks(id_user, count=100)
      for network_ in user_networks:
        if int(id_network) == int(network_['id']):
          user_is_member = True
          break

  network_info = {}
  network_info['id'] = id_network
  network_info['posts'] = recent_posts
  network_info['events'] = recent_events
  network_info['network_title'] = get_network_title(network)
  network_info['user_is_member'] = user_is_member

  if user_is_member and scenario == 'normal':
    network_info['greeting'] = 'You are a member of this network.  Welcome!'
  elif not user_is_member and scenario == 'normal':
    network_info['greeting'] = 'You are not a member of this network. Join now to create posts and events.'
  elif user_is_member and scenario == 'join':
    network_info['greeting'] = 'You just joined this network. Welcome!'
  elif not user_is_member and scenario == 'join':
    network_info['greeting'] = 'Looks like something went wrong. Try joining later.'
  elif user_is_member and scenario == 'leave':
    network_info['greeting'] = 'Looks like something went wrong. Try leaving later.'
  elif not user_is_member and scenario == 'leave':
    network_info['greeting'] = 'You just left this network. Bye bye!'

  num_users = client.get_network_user_count(id_network)['user_count']
  num_posts = client.get_network_post_count(id_network)['post_count']

  network_info['num_users'] = num_users
  network_info['num_posts'] = num_posts
  return network_info
