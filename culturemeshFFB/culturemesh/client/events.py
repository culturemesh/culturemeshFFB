#
# CultureMesh Event API
#

from .client import Request

####################### GET methods #######################

def ping_event(client):
    url = '/event/ping'
    return client._request(url, Request.GET)

def get_event(client, eventId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event to fetch

	Returns an event by ID.
	"""
	url = '/event/%s' % str(eventId)
	return client._request(url, Request.GET)

def get_event_registration_list(client, eventId, count, max_register_date=None):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event in question
	:param count: the number of results to return
	:param max_register_date: the maximum register date, inclusive, to return
	                          events for.

	Returns a list of user JSONs registered to this event.
	"""
	url = '/event/%s/reg' % str(eventId)
	query_params = {'count': count}
	if max_register_date:
		query_params['max_register_date'] = max_register_date

	# TODO: need to URL escape the query parameters with spaces.
	return client._request(url, Request.GET, query_params=query_params)

def get_events_attending_in_network(client, current_user,
									network_id, count, max_id=None):
	"""
	:param client: the CultureMesh API client
	:param network_id: the id of the event to fetch
	:param count: the max number of results to return
	:param max_id: the maximum id, inclusive, to return events for.

	Returns events the current user is attending in this network.
	"""
	url = '/event/currentUserEventsByNetwork/%s' % str(network_id)
	query_params = {'count': count}
	if max_id:
		query_params['max_id'] = max_id
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.GET, query_params=query_params, basic_auth=basic_auth
	)

def get_event_reg_count(client, event_id):
	"""
	:param client: the CultureMesh API client
	:param event_id: the id of the event to fetch the registration count for.

	Returns the number of people registered for an event.
	"""
	url = '/event/%s/reg_count' % str(event_id)
	return client._request(url, Request.GET)

####################### POST methods #######################

def create_event(client, current_user, event):
	"""
	:param client: the CultureMesh API client
	:param current_user: the current user
	:param event: the JSON of the event to create

	Creates a new event.
	"""
	url = '/event/new'
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.POST, json=event, basic_auth=basic_auth
	)

####################### PUT methods #######################

def update_event(client, current_user, event):
	"""
	:param client: the CultureMesh API client
	:param current_user: the current user
	:param event: the JSON of the event to update

	Updates an event.
	"""
	url = '/event/new'
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.PUT, json=event, basic_auth=basic_auth
	)

####################### DELETE methods #######################

def delete_event(client, current_user, event_id):
	"""
	:param client: the CultureMesh API client
	:param current_user: the current user object
	:param event_id: the id of the event to delete.

	Deletes an event and unregisters everyone from it.
	"""
	url = 'event/delete'
	query_params = {'id': str(event_id)}
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.DELETE, query_params=query_params, basic_auth=basic_auth
	)
