#
# CultureMesh Users API
#

from .client import Request

####################### GET methods #######################

def ping_user(client):
    url = 'user/ping'
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
	url = 'users'
	return client._request(url, Request.GET, body_data=params,
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
	url = 'user/%s/networks' % str(user_id)
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
	:param role: can be "host" or "guest"

	Returns list of events related to USER_ID, according to ROLE.
	"""
	query_params = {'role': role, 'count': count}
	url = 'user/%s/events' % str(user_id)
	if max_id is not None:
		query_params['max_id'] = max_id
	return client._request(url, Request.GET, query_params=query_params)

def get_user_events_hosting(client, user_id, count, max_id=None):
	return get_user_events(client, user_id, "host", count, max_id)

def get_user_events_attending(client, user_id, count, max_id=None):
	return get_user_events(client, user_id, "guest", count, max_id)


####################### POST methods #######################

def create_user(client, user):
	"""
	:param client: the CultureMesh API client
	:param user: the user JSON to create.

	Creates a new user.
	"""
	url = 'user/users'
	return client._request(url, Request.POST, json=user)

def join_event_as_guest(client, current_user, event_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param eventId: The id of the event to register this user to

	Registers a user to a attend an event as a guest.
	"""
	url = 'user/joinEvent/%s' % str(event_id)
	basic_auth = (str(current_user.api_token), "")
	query_params = {}
	query_params['role'] = "guest"
	return client._request(
		url, Request.POST, basic_auth=basic_auth, query_params=query_params
	)

def join_event_as_host(client, current_user, event_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param eventId: The id of the event to register this user to

	Registers a user to a attend an event as a host.
	"""
	url = 'user/joinEvent/%s' % str(event_id)
	basic_auth = (str(current_user.api_token), "")
	query_params = {}
	query_params['role'] = "host"
	return client._request(
		url, Request.POST, basic_auth=basic_auth, query_params=query_params
	)

def join_network(client, current_user, network_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param networkId: The id of the network to add user to

	Adds a user to a network.
	"""
	url = 'user/joinNetwork/%s' % str(network_id)
	basic_auth = (str(current_user.api_token), "")
	return client._request(url, Request.POST, basic_auth=basic_auth)

####################### DELETE methods ####################

def leave_event(client, current_user, event_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param event_id: The id of the event to leave

	Removes a user from an event.
	"""
	url = 'user/leaveEvent/%s' % str(event_id)
	basic_auth = (str(current_user.api_token), "")
	return client._request(url, Request.DELETE, basic_auth=basic_auth)

def leave_network(client, current_user, network_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param network_id: The id of the network to leave

	Removes a user from a network.
	"""
	url = 'user/leaveNetwork/%s' % str(network_id)
	basic_auth = (str(current_user.api_token), "")
	return client._request(url, Request.DELETE, basic_auth=basic_auth)


####################### PUT methods #######################

def update_user(client, current_user, user):
	"""
	:param client: the CultureMesh API client
    :param current_user: the current CultureMesh user
	:param user: A user JSON to update an existing user with.

	Updates the information of a user.
	"""
	url = 'user/update_user'
	basic_auth = (str(current_user.api_token), "")
	return client._request(
            url, Request.PUT, json=user, basic_auth=basic_auth
    )
