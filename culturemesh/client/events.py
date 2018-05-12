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
	if max_register_date is not None:
		query_params['max_register_date'] = max_register_date

	# TODO: need to URL escape the query parameters with spaces.
	return client._request(url, Request.GET, query_params=query_params)

####################### POST methods #######################

def create_event(client, event):
	"""
	:param client: the CultureMesh API client
	:param event: the JSON of the event to create

	Creates a new event.
	"""
	raise NotImplementedError

####################### PUT methods #######################

def update_event(client, event):
	"""
	:param client: the CultureMesh API client
	:param event: the JSON of the event to update

	Updates an event.
	"""
	raise NotImplementedError
