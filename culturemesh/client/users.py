#
# CultureMesh Users API
#

####################### GET methods #######################

from .client import Request

def ping_user(client):
    url = '/user/ping'
    return client._request(url, Request.GET)

def get_users(client, count, max_id=None, filter_=None):
	"""
	:param client: the CultureMesh API client
	:param count: the number of results to return
	:param max_id: the maximum id, inclusive, of users to fetch
	:param filter: A json with which to filter a site-wide user query.

	Returns a list of users filtered by FILTER, sorted in reverse
	order by id.
	"""
	params = {'filter': filter_}
	query_params = {'count': count}
	if max_id is not None:
		query_params['max_id'] = max_id
	url = '/users'
	return client._request(url, Request.GET, body_params=params,
		query_params=query_params)

def get_user(client, userId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return.

	Returns JSON of user.
	"""
	url = '/user/%s' % str(userId)
	return client._request(url, Request.GET)

def get_user_networks(client, user_id, count, max_register_date=None):
	"""
	:param client: the CultureMesh API client
	:param user_id: The id of the user to return a list of networks for.
	:param count: the number of results to return
	:param max_register_date: the maximum network register date, inclusive,
														to return networks for.

	Returns list of network JSONs to which USER_ID belongs.
	"""
	url = '/user/%s/networks' % str(user_id)
	query_params = {'count': count}
	if max_register_date is not None:
		query_params['max_register_date'] = max_register_date
	return client._request(url, Request.GET, query_params=query_params)

def get_user_posts(client, user_id, count, max_id=None):
	"""
	:param client: the CultureMesh API client
	:param userId: user ID to return posts for
	:param count: the number of results to return
	:param max_id: the maximum id, inclusive, of posts to fetch

	Returns list of post JSONs authored by USER_ID,
	sorted in reverse order by id.
	"""
	url = '/user/%s/posts' % str(user_id)
	query_params = {'count': count}
	if max_id is not None:
		query_params['max_id'] = max_id
	return client._request(url, Request.GET, query_params=query_params)

def get_user_events(client, user_id, role, count, max_id=None):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to return events for.
	:param role: can be "hosting" or "attending"

	Returns list of events related to USER_ID, according to ROLE.
	"""
	query_params = {'role': role, 'count': count}
	url = '/user/%s/events' % str(user_id)
	if max_id is not None:
		query_params['max_id'] = max_id
	return client._request(url, Request.GET, query_params=query_params)


####################### POST methods #######################

def create_user(client, user):
	"""
	:param client: the CultureMesh API client
	:param user: the user JSON to create.

	Creates a new user.
	"""
	params = {"user": user}
	url = '/user'
	return client._request(url, Request.POST, body_params=params)

def add_user_to_event(client, userId, eventId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to to add
	:param eventId: The id of the event to register this user to

	Registers a user to a attend an event.
	"""
	url = '/user/%s/addToEvent/%s' % (str(userId), str(eventId))
	return client._request(url, Request.POST)

def add_user_to_network(client, userId, networkId):
	"""
	:param client: the CultureMesh API client
	:param userId: The id of the user to add
	:param networkId: The id of the network to add user to

	Adds a user to a network.
	"""
	url = '/user/%s/addToNetwork/%s' % (str(userId), str(networkId))
	return client._request(url, Request.POST)

####################### PUT methods #######################

def update_user(client, user):
	"""
	:param client: the CultureMesh API client
	:param user: A user JSON to update an existing user with.

	Updates the information of a user.
	"""
	params = {'user': user}

	raise NotImplementedError
	url = '/user'
	return client._request(url, Request.PUT, body_params=params)
