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
import datetime
import config
import culturemesh
from culturemesh import app
from difflib import SequenceMatcher
from flask import abort
from urllib.parse import urlparse
from enum import IntEnum

# Relative from app.root_path
USER_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_users.json")
POST_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_posts.json")
POST_REPLY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_post_replies.json")
EVENT_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_events.json")
EVENT_REGISTRATION_LOC = os.path.join(app.root_path, "../data/mock/db_mock_event_registration.json")
NET_REGISTRATION_LOC = os.path.join(app.root_path, "../data/mock/db_mock_network_registration.json")
NETWORK_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_networks.json")
LANG_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_languages.json")
CITY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_cities.json")
REGION_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_regions.json")
COUNTRY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_countries.json")
KEY = os.environ['CULTUREMESH_API_KEY']

class Request(IntEnum):
	GET = 1
	POST = 2
	PUT = 3
	DELETE = 4

class Client(object):
	"""Talks directly to the CultureMesh API.
	"""
	_api_base_url_ = os.environ["CULTUREMESH_API_BASE_ENDPOINT"]

	def __init__(self, key=None, client_id=None, client_secret=None,
				 timeout=None, connect_timeout=None, read_timeout=None,
				 retry_timeout=60, queries_per_second=10,
				 channel=None, mock=True):


		self.mock = mock
		# See: http://docs.python-requests.org/en/master/user/advanced/
		#	  not used yet.
		self.session = requests.Session()

	def _request(self,
				 url,
				 request_method,
				 query_params=None,
				 body_data=None,
				 json=None,
				 body_extractor=None,
				 basic_auth=None):
		"""
		Carries out HTTP requests.

		Returns body as JSON.
		"""
		if self.mock:
			return self._mock_request(url, query_params, body_data)

		# This is always controlled by us, not by the user.
		url = "%s/%s?key=%s" % (self._api_base_url_, url, KEY)
		if query_params is not None:
			for param in query_params:
				url += "&%s=%s" % (param, query_params[param])

		if request_method == Request.GET:
			response = requests.get(url, auth=basic_auth)
		elif request_method == Request.POST:
			response = requests.post(
				url, json=json, data=body_data, auth=basic_auth
			)
		elif request_method == Request.PUT:
			response = requests.put(
				url, json=json, data=body_data, auth=basic_auth
			)
		elif request_method == Request.DELETE:
			response = requests.delete(
				url, json=json, data=body_data, auth=basic_auth
			)
		return self._get_body(response)

	def _get_body(self, response):
		"""
		Gets the JSON body of a response.

		Raises HTTPError exceptions.
		"""
		if response.status_code != 200:
			abort(response.status_code)
		try:
			return response.json()
		except json.decoder.JSONDecodeError:
			return response.text

	########################### MOCK DATA METHODS BELOW ##########################

	def _mock_request(self, url, query_params, body_params):
		"""
		Used in development and for unit testing.
		Uses local data to return API responses.

		Warning: VERY AD HOC.
		"""

		url_ = urlparse(url)
		path = os.path.normpath(url_.path).split(os.sep)
		if path[0] == '':
			path = path[1:]

		module = path[0]
		path_len = len(path)

		if path_len == 1:
			if module == "users":
				if body_params and "filter" in body_params and body_params["filter"]:
					raise NotImplementedError("Sorry. Can't filter.")
				return self._mock_get_users(query_params)

		elif path_len == 2:
			if module == "network":

				if path[1] == "networks":
					return self._mock_get_networks(
						query_params, body_params
					)
				else:
					network_id = int(path[1])
					return self._mock_get_network(network_id)

			elif module == "post":
				post_id = int(path[1])
				return self._mock_get_post(post_id)

			elif module == "user":
				id_user = int(path[1])
				return self._mock_get_user(id_user)

			elif module == "event":
				event_id = int(path[1])
				return self._mock_get_event(event_id)

			elif module == "language":
				if path[1] == "autocomplete":
					input_text = query_params['input_text']
					return self._mock_language_autocomplete(input_text)
				else:
					lang_id = int(path[1])
					return self._mock_get_language(lang_id)

			elif module == "location":
				if path[1] == "autocomplete":
					input_text = query_params['input_text']
					return self._mock_location_autocomplete(input_text)


		elif path_len == 3:
			if module == "post":
				if path[2] == "replies":
					return self._mock_get_post_replies(int(path[1]), query_params)

			elif module == "user":
				if path[2] == "posts":
					return self._mock_get_user_posts(int(path[1]), query_params)

				elif path[2] == "events":
					if query_params['role'] != "hosting":
						raise NotImplementedError("Currently, can only get events a user is hosting.")
					return self._mock_get_user_events_hosting(int(path[1]), query_params)

				elif path[2] == "networks":
					return self._mock_get_user_networks(int(path[1]), query_params)

			elif module == "location":
				if path[1] == "cities":
					city_id = int(path[2])
					return self._mock_get_city(city_id)

				elif path[1] == "regions":
					region_id = int(path[2])
					return self._mock_get_region(region_id)

				elif path[1] == "countries":
					country_id = int(path[2])
					return self._mock_get_country(country_id)

			elif module == "event":
				if path[2] == "reg":
					event_id = int(path[1])
					return self._mock_get_event_registration(event_id, query_params)

			elif module == "network":
				if path[2] == "posts":
					return self._mock_get_network_posts(int(path[1]), query_params)
				elif path[2] == "events":
					return self._mock_get_network_events(int(path[1]), query_params)
				elif path[2] == "users":
					return self._mock_get_network_users(int(path[1]), query_params)

		raise NotImplementedError(
			"Sorry.  Can't get mock data for path '%s'" % "/".join(path)
		)

	def _mock_str_to_date(self, str_):
		return datetime.datetime.strptime(str_, config.DATETIME_FMT_STR)

	def _mock_ensure_count(self, query_params):
		if 'count' not in query_params:
			raise AttributeError("count field missing in query parameters")

		count = int(query_params['count'])
		if count < 1 or count > 100:
			raise AttributeError("Invalid count field.")

	def _mock_get_users(self, query_params):
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(USER_DATA_LOC) as users:
			users = sorted(json.load(users), key=lambda x: x['id'], reverse=True)
			max_id = users[0]['id']
			if 'max_id' in query_params:
				max_id = query_params['max_id']

			result = []
			for u in users:
				if count == 0:
					break
				if u['id'] <= max_id:
					result.append(u)
					count -= 1

			return result

	def _mock_get_user(self, id_user):
		with open(USER_DATA_LOC) as users:
			users = json.load(users)
			for u in users:
				if u['id'] == id_user:
					return u

	def _mock_get_user_networks(self, id_user, query_params):
		"""
		Returns mock list of networks a user belongs to. Returns the most recently
		joined networks first.
		"""
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(NET_REGISTRATION_LOC) as network_reg:
			user_network_regs = []
			network_reg = json.load(network_reg)
			for n_reg in network_reg:
				if n_reg['id_user'] == id_user:
					user_network_regs.append(n_reg)

			if len(user_network_regs) == 0:
				return []

			# Sort in reverse join-date order, i.e. latest joins go first
			user_network_regs = sorted(
				user_network_regs,
				key=lambda x: self._mock_str_to_date(x['join_date']),
				reverse=True
			)

			max_date = self._mock_str_to_date(user_network_regs[0]['join_date'])
			if 'max_register_date' in query_params:
				max_date = self._mock_str_to_date(query_params['max_register_date'])

			# Construct the id's of the networks according to pagination
			network_ids = []
			for n in user_network_regs:
				if count == 0:
					break

				if self._mock_str_to_date(n['join_date']) <= max_date:
					network_ids.append(n['id_network'])
					count -= 1

			# Fetch the network objects
			networks = []
			for network_id in network_ids:
				network = self._mock_get_network(network_id)
				if network is not None:
					networks.append(network)
			return networks

	def _mock_get_user_posts(self, id_user, query_params):
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(POST_DATA_LOC) as posts:
			user_posts = []
			posts = json.load(posts)
			for p in posts:
				if p['id_user'] == id_user:
					user_posts.append(p)

			if len(user_posts) == 0:
				return user_posts

			# Sort in reverse id order.
			user_posts = sorted(user_posts, key=lambda x: x['id'], reverse=True)
			max_id = user_posts[0]['id']
			if 'max_id' in query_params:
				max_id = query_params['max_id']

			res = []
			for p in user_posts:
				if count == 0:
					break
				if p['id'] <= max_id:
					res.append(p)
					count -= 1

			return res

	def _mock_get_user_events_hosting(self, id_user, query_params):
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(EVENT_DATA_LOC) as events:
			user_hosting = []
			events = json.load(events)
			for e in events:
				if e['id_host'] == id_user:
					user_hosting.append(e)
			if len(user_hosting) == 0:
				return user_hosting

			user_hosting = sorted(user_hosting, key=lambda x: x['id'], reverse=True)
			max_id = user_hosting[0]['id']
			if 'max_id' in query_params:
				max_id = query_params['max_id']

			res = []
			for e in user_hosting:
				if count == 0:
					break
				if e['id'] <= max_id:
					res.append(e)
					count -= 1
			return res

	def _pagination(self, query_params, objects, key='id'):
		""" Pagination """
		self._mock_ensure_count(query_params)
		count = query_params['count']
		if len(objects) == 0:
			return objects

		# Sort in reverse id order.
		objects = sorted(objects, key=lambda x: x[key], reverse=True)
		max_id = objects[0][key]
		if 'max_id' in query_params:
			max_id = query_params['max_id']

		res = []
		for p in objects:
			if count == 0:
				break
			if p[key] <= max_id:
				res.append(p)
				count -= 1

		return res

	def filter_networks(self, filter_params, networks):
		"""
			Rank networks based on search parameters
		"""
		def similarity(a, b):
		    return SequenceMatcher(None, a, b).ratio()
		cities = {c["id"]:c["name"] for c in json.load(open(CITY_DATA_LOC))}
		countries = {c["id"]:c["name"] for c in json.load(open(COUNTRY_DATA_LOC))}
		regions = {r["id"]:r["name"] for r in json.load(open(REGION_DATA_LOC))}
		N = len(networks)
		query_near = filter_params["near"]
		networks_cur_countries = [countries[net["location_cur"]["country_id"]] for net in networks]
		networks_cur_cities = [cities[net["location_cur"]["city_id"]] for net in networks]
		networks_cur_regions = [regions[net["location_cur"]["region_id"]] for net in networks]
		near_similarity = {}
		near_similarity["countries"] = [similarity(query_near, c) for c in networks_cur_regions]
		near_similarity["cities"] = [similarity(query_near, c) for c in networks_cur_cities]
		near_similarity["regions"] = [similarity(query_near, r) for r in networks_cur_regions]
		near_similarity = [max(near_similarity["countries"][k], near_similarity["cities"][k],
						near_similarity["regions"][k]) for k in range(N)]
		if filter_params["search_type"] == "location":
			query_from = filter_params["from"]
			networks_orig_countries = [countries[net["location_origin"]["country_id"]] for net in networks]
			networks_orig_cities = [cities[net["location_origin"]["city_id"]] for net in networks]
			networks_orig_regions = [regions[net["location_origin"]["region_id"]] for net in networks]
			from_similarity = {}
			from_similarity["countries"] = [similarity(query_from, c) for c in networks_orig_regions]
			from_similarity["cities"] = [similarity(query_from, c) for c in networks_orig_cities]
			from_similarity["regions"] = [similarity(query_from, r) for r in networks_orig_regions]
			from_similarity = [max(from_similarity["countries"][k], from_similarity["cities"][k],
							from_similarity["regions"][k]) for k in range(N)]
			similarity = [(near_similarity[k] + from_similarity[k])/2 for k in range(N)]
		elif filter_params["search_type"] == "language":
			query_language = filter_params["language"]
			networks_languages = [net["language_origin"]["name"] for net in networks]
			language_similarity = [similarity(query_language, l) for l in networks_languages]
			similarity = [(near_similarity[k] + language_similarity[k])/2 for k in range(N)]
		else:
			raise Exception("Invalid Network search type")
		for i, net in enumerate(networks):
			net["search_rank"] = similarity[i]

	def _mock_get_networks(self, query_params, body_params):
		with open(NETWORK_DATA_LOC) as networks:
			networks = sorted(json.load(networks), key=lambda x: x['id'], reverse=True)
			networks = self._pagination(query_params, objects=networks, key='id')
			if body_params and "filter" in body_params and body_params["filter"]:
				self.filter_networks(body_params["filter"], networks)
				networks = sorted(networks, key=lambda x: x['search_rank'], reverse=True)
			return networks


	def _mock_get_network(self, network_id):
		"""
		Returns mock data for a single
		network.
		"""
		with open(NETWORK_DATA_LOC) as networks:
			networks = json.load(networks)
			for n in networks:
				if n['id'] == network_id:
					return n

	def _mock_get_network_posts(self, network_id, query_params):
		with open(POST_DATA_LOC) as posts:
			network_posts = []
			posts = json.load(posts)
			for p in posts:
				if p['id_network'] == network_id:
					network_posts.append(p)
			return self._pagination(query_params, objects=network_posts, key='id')

	def _mock_get_network_events(self, network_id, query_params):
		"""
		Returns events associated with this
		"""
		with open(EVENT_DATA_LOC) as events:
			network_events = []
			events = json.load(events)
			for p in events:
				if p['id_network'] == network_id:
					network_events.append(p)
			return self._pagination(query_params, objects=network_events, key='id')

	def _mock_get_network_users(self, network_id, query_params):
		"""
		Return mock list of network registration jsons associated with the network.
		"""
		with open(NET_REGISTRATION_LOC) as registrations:
			network_registration = []
			registrations = json.load(registrations)
			for p in registrations:
				if p['id_network'] == network_id:
					network_registration.append(p)
			return self._pagination(query_params, objects=network_registration, key='join_date')

	def _mock_get_post(self, post_id):
		with open(POST_DATA_LOC) as posts:
			posts = json.load(posts)
			for p in posts:
				if p['id'] == post_id:
					return p
			return None

	def _mock_get_post_replies(self, post_id, query_params):
		"""
		Returns mock list of post replies to this
		post.
		"""
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(POST_REPLY_DATA_LOC) as post_replies:
			post_replies_ = []
			post_replies = json.load(post_replies)
			for p in post_replies:
				if p['id_parent'] == post_id:
					post_replies_.append(p)

			if len(post_replies_) == 0:
				return post_replies_

			post_replies_ = sorted(post_replies_, key=lambda x: x['id'], reverse=True)
			max_id = post_replies_[0]['id']
			if 'max_id' in query_params:
				max_id = query_params['max_id']

			res = []
			for repl in post_replies_:
				if count == 0:
					break
				if repl['id'] <= max_id:
					res.append(repl)
					count -= 1
			return res

	def _mock_get_event(self, event_id):
		"""
		Returns this mock event.
		"""
		with open(EVENT_DATA_LOC) as events:
			events = json.load(events)
			for e in events:
				if e['id'] == event_id:
					return e
			return None

	def _mock_get_event_registration(self, event_id, query_params):
		"""
		Returns mock list of users attending
		this event.
		"""
		self._mock_ensure_count(query_params)
		count = query_params['count']
		with open(EVENT_REGISTRATION_LOC) as event_regs:
			event_regs_ = []
			event_regs = json.load(event_regs)
			for reg in event_regs:
				if reg['id_event'] == event_id:
					event_regs_.append(reg)

			if len(event_regs_) == 0:
				return event_regs_

			sort_key = lambda x: self._mock_str_to_date(x['date_registered'])
			event_regs_ = sorted(event_regs_, key=sort_key, reverse=True)
			max_date = self._mock_str_to_date(event_regs_[0]['date_registered'])
			if 'max_register_date' in query_params:
				max_date = self._mock_str_to_date(query_params['max_register_date'])

			res = []
			for e in event_regs_:
				if count == 0:
					break

				if self._mock_str_to_date(e['date_registered']) <= max_date:
					res.append(e)
					count -= 1
			return res

	def _mock_get_city(self, city_id):
		"""
		Returns mock data for this city.
		"""
		with open(CITY_DATA_LOC) as cities:
			cities = json.load(cities)
			for c in cities:
				if c['id'] == city_id:
					return c
			return None

	def _mock_get_region(self, region_id):
		"""
		Returns mock data for this region.
		"""
		with open(REGION_DATA_LOC) as regions:
			regions = json.load(regions)
			for r in regions:
				if r['id'] == region_id:
					return r
			return None

	def _mock_get_country(self, country_id):
		"""
		Returns mock data for country.
		"""
		with open(COUNTRY_DATA_LOC) as countries:
			countries = json.load(countries)
			for c in countries:
				if c['id'] == country_id:
					return c
			return None

	def _mock_location_autocomplete(self, input_text):
		"""
		Returns mock autocomplete entries for input_text.
		"""
		return input_text + " + [location autocompleted text]"

	def _mock_get_language(self, lang_id):
		"""
		Returns mock data for language.
		"""
		with open(LANG_DATA_LOC) as langs:
			langs = json.load(langs)
			for l in langs:
				if l['id'] == lang_id:
					return l
			return None

	def _mock_language_autocomplete(self, input_text):
		"""
		Returns mock autocomplete entries for language input.
		"""
		return input_text + " + [language autocompleted text]"

""" Register the client with the API functions. """
from .accounts import get_token
from .events import ping_event
from .events import get_event
from .events import get_event_registration_list
from .events import get_event_reg_count
from .events import create_event
from .events import update_event
from .events import delete_event
from .events import get_events_attending_in_network
from .languages import get_language
from .languages import language_autocomplete
from .locations import get_city
from .locations import get_region
from .locations import get_country
from .locations import location_autocomplete
from .posts import ping_post
from .posts import get_post
from .posts import get_post_reply
from .posts import get_post_replies
from .posts import get_post_reply_count
from .posts import create_post
from .posts import create_post_reply
from .posts import update_post
from .posts import update_post_reply
from .users import ping_user
from .users import get_users
from .users import get_user
from .users import get_user_networks
from .users import get_user_posts
from .users import get_user_events
from .users import get_user_events_hosting
from .users import get_user_events_attending
from .users import create_user
from .users import join_event_as_host
from .users import join_event_as_guest
from .users import leave_event
from .users import join_network
from .users import leave_network
from .users import update_user
from .networks import ping_network
from .networks import get_networks
from .networks import get_network
from .networks import get_network_posts
from .networks import get_network_events
from .networks import get_network_users
from .networks import get_network_user_count
from .networks import get_network_post_count

# We may consider adding a wrapper around these assignments
# below to introduce more specific features for the client.

Client.get_token = get_token
Client.ping_event = ping_event
Client.get_event = get_event
Client.get_event_registration_list = get_event_registration_list
Client.get_event_reg_count = get_event_reg_count
Client.create_event = create_event
Client.update_event = update_event
Client.delete_event = delete_event
Client.get_events_attending_in_network = get_events_attending_in_network
Client.get_language = get_language
Client.language_autocomplete = language_autocomplete
Client.get_city = get_city
Client.get_region = get_region
Client.get_country = get_country
Client.location_autocomplete = location_autocomplete
Client.ping_post = ping_post
Client.get_post = get_post
Client.get_post_reply = get_post_reply
Client.get_post_replies = get_post_replies
Client.get_post_reply_count = get_post_reply_count
Client.create_post = create_post
Client.create_post_reply = create_post_reply
Client.update_post = update_post
Client.update_post_reply = update_post_reply
Client.ping_user = ping_user
Client.get_users = get_users
Client.get_user = get_user
Client.get_user_networks = get_user_networks
Client.get_user_posts = get_user_posts
Client.get_user_events = get_user_events
Client.get_user_events_hosting = get_user_events_hosting
Client.get_user_events_attending = get_user_events_attending
Client.create_user = create_user
Client.join_event_as_guest = join_event_as_guest
Client.join_event_as_host = join_event_as_host
Client.leave_event = leave_event
Client.join_network = join_network
Client.leave_network = leave_network
Client.update_user = update_user
Client.ping_network = ping_network
Client.get_networks = get_networks
Client.get_network = get_network
Client.get_network_posts = get_network_posts
Client.get_network_events = get_network_events
Client.get_network_users = get_network_users
Client.get_network_user_count = get_network_user_count
Client.get_network_post_count = get_network_post_count
