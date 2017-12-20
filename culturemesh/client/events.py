#
# CultureMesh Event API
#

from .client import Request

####################### GET methods #######################

def get_event(client, eventId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event to fetch

	Returns an event by ID.
	"""
	url = '/event/%s' % str(eventId)
	return client._request(url, Request.GET)

def get_event_registration_list(client, eventId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the id of the event in question

	Returns a list of user JSONs registered to this event.
	"""
	url = '/event/%s/reg' % str(eventId)
	return client._request(url, Request.GET)

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