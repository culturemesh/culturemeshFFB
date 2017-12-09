#
# CultureMesh API Client
#
# Inspired by: https://github.com/googlemaps/google-maps-services-python
# TODO: add license information.
#

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import requests
import os
import json
from urllib.parse import urlparse

from enum import IntEnum

USER_DATA_LOC_RELATIVE = "../data/db_mock_users.json"
POST_DATA_LOC_RELATIVE = "../data/db_mock_posts.json"
EVENT_DATA_LOC_RELATIVE = "../data/db_mock_events.json"
NETWORK_DATA_LOC_RELATIVE = "../data/db_mock_networks.json"

class Request(IntEnum):
	GET = 1
	POST = 2
	PUT = 3

class Client(object):
	""" Talks directly to CultureMesh """

	_api_base_url_ = "www.culturemesh.com/api/v1/"

	def __init__(self, key=None, client_id=None, client_secret=None,
                 timeout=None, connect_timeout=None, read_timeout=None,
                 retry_timeout=60, queries_per_second=10,
                 channel=None, mock=True):

		# TODO: insert client initialization here.
		self.mock = mock

		# See: http://docs.python-requests.org/en/master/user/advanced/
		#      not used yet.
		self.session = requests.Session()

	def _request(self, url, request_method, query_params=None, body_params=None,
				 post_json=None, body_extractor=None):
		"""
		Carries out HTTP requests.

		Returns body as JSON.
    	"""
		if self.mock:
			return self._mock_request(url, query_params, body_params)
		raise NotImplementedError("Real API coming soon.")

	def _get_body(self, response):
		"""
		Gets the JSON body of a response.

		Raises HTTPError exceptions.
		"""
		if response.status_code != 200:
			raise culturemesh.exceptions.HTTPError(response.status_code)

		return response.json()

	########################### MOCK DATA METHODS BELOW ###############################

	def _mock_request(self, url, query_params, body_params):
		"""
		Used in development.  Uses local data to return API responses.

		Warning: VERY AD HOC.
		"""

		url_ = urlparse(url)
		path = os.path.normpath(url_.path).split(os.sep)
		print(path)
		if len(path) == 2:
			if path[1] == "users":
				if body_params and "filter" in body_params and body_params["filter"]:
					raise NotImplementedError("Sorry. Can't filter.")
				return self._mock_get_all_users()
			elif path[1] == "networks":
				if body_params and "filter" in body_params and body_params["filter"]:
					raise NotImplementedError("Sorry. Can't filter.")
				return self._mock_get_all_networks()
		elif len(path) == 3:
			if path[1] == "user":
				user_id = int(path[2])
				return self._mock_get_user(user_id)

			elif path[1] == "post":
				post_id = int(path[2])
				return self._mock_get_post(post_id)

		elif len(path) == 4:
			if path[1] == "user":
				if path[3] == "posts":
					return self._mock_get_user_posts(int(path[2]))
				elif path[3] == "events":
					if query_params['role'] != "hosting":
						raise NotImplementedError("Can only get events a user is hosting.")

					return self._mock_get_user_events_hosting(int(path[2]))
			else:
				pass
		elif len(path) == 5:
			pass

		raise NotImplementedError("Sorry.  Can't get that mock data yet!")


	def _mock_get_all_users(self):
		with open(USER_DATA_LOC_RELATIVE) as users:
			return json.load(users)

	def _mock_get_user(self, user_id):
		with open(USER_DATA_LOC_RELATIVE) as users:
			users = json.load(users)
			for u in users:
				if u['user_id'] == user_id:
					return u

	def _mock_get_user_networks(self, user_id):
		"""
		Returns mock list of networks a user belongs to. 
		"""
		raise NotImplementedError

	def _mock_get_user_posts(self, user_id):
		with open(POST_DATA_LOC_RELATIVE) as posts:
			user_posts = []
			posts = json.load(posts)
			for p in posts:
				if p['user_id'] == user_id:
					user_posts.append(p)
			return user_posts

	def _mock_get_user_events_hosting(self, user_id):
		with open(EVENT_DATA_LOC_RELATIVE) as events:
			user_hosting = []
			events = json.load(events)
			for e in events:
				if e['host_id'] == user_id:
					user_hosting.append(e)
			return user_hosting

	def _mock_get_all_networks(self):
		with open(NETWORK_DATA_LOC_RELATIVE) as networks:
			return json.load(networks)

	def _mock_get_network(self, network_id):
		"""
		Returns mock data for a single 
		network. 
		"""
		raise NotImplementedError

	def _mock_get_network_events(self, network_id):
		"""
		Returns all events associated with this 
		network. 
		"""
		raise NotImplementedError

	def _mock_get_network_users(self, network_id):
		"""
		Return mock list of user jsons in the network. 
		"""
		raise NotImplementedError

	def _mock_get_post(self, post_id):
		with open(POST_DATA_LOC_RELATIVE) as posts:
			posts = json.load(posts)
			for p in posts:
				if p['id'] == post_id:
					return p
			return None

	def _mock_get_post_replies(self, post_id):
		"""
		Returns mock list of post replies to this
		post. 
		"""
		raise NotImplementedError

	def _mock_get_event(self, event_id):
		"""
		Returns this mock event. 
		"""
		raise NotImplementedError

	def _mock_get_event_attendance(self, event_id):
		"""
		Returns mock list of users attending
		this event. 
		"""
		raise NotImplementedError

	def _mock_get_city(self, city_id):
		"""
		Returns mock data for this city. 
		"""
		raise NotImplementedError

	def _mock_get_region(self, region_id):
		"""
		Returns mock data for this region. 
		"""
		raise NotImplementedError

	def _mock_get_country(self, country_id):
		"""
		Returns mock data for country. 
		"""
		raise NotImplementedError

	def _mock_location_autocomplete(self, input_text):
		"""
		Returns mock autocomplete entries for input_text. 
		"""
		raise NotImplementedError

	def _mock_get_language(self, lang_id):
		"""
		Returns mock data for language. 
		"""
		raise NotImplementedError

	def _mock_language_autocomplete(self, input_text):
		"""
		Returns mock autocomplete entries for language input. 
		"""
		raise NotImplementedError


""" Register the client with the API functions. """

from .example_api_module import get_gutenberg_novel
from .events import get_event
from .events import get_event_attendance_list
from .events import create_event
from .events import update_event
from .languages import get_language
from .languages import language_autocomplete
from .locations import get_city
from .locations import get_region
from .locations import get_country
from .locations import location_autocomplete
from .posts import get_post
from .posts import get_post_replies
from .posts import create_post
from .posts import create_post_reply
from .users import get_users
from .users import get_user
from .users import get_user_networks
from .users import get_user_posts
from .users import get_user_events
from .users import create_user
from .users import add_user_to_event
from .users import add_user_to_network
from .users import update_user
from .networks import get_networks

# We may consider adding a wrapper around these assignments
# below to introduce more specific features for the client.

Client.get_gutenberg_novel = get_gutenberg_novel
Client.get_event = get_event
Client.get_event_attendance_list = get_event_attendance_list
Client.create_event = create_event
Client.update_event = update_event
Client.get_language = get_language
Client.language_autocomplete = language_autocomplete
Client.get_city = get_city
Client.get_region = get_region
Client.get_country = get_country
Client.location_autocomplete = location_autocomplete
Client.get_post = get_post
Client.get_post_replies = get_post_replies
Client.create_post = create_post
Client.create_post_reply = create_post_reply
Client.get_users = get_users
Client.get_user = get_user
Client.get_user_networks = get_user_networks
Client.get_user_posts = get_user_posts
Client.get_user_events = get_user_events
Client.create_user = create_user
Client.add_user_to_event = add_user_to_event
Client.add_user_to_network = add_user_to_network
Client.update_user = update_user
Client.get_networks = get_networks
