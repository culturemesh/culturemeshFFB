#
# CultureMesh Locations API 
#

from .client import Request

####################### GET methods #######################

def get_city(client, cityId):
	"""
	:param client: the CultureMesh API client
	:param cityId: the id of the city to fetch.

	Returns a city JSON.
	"""
	url = '/location/cities/%s' % str(cityId)
	return client._request(url, Request.GET)

def get_region(client, regionId):
	"""
	:param client: the CultureMesh API client
	:param regionId: the id of the region to fetch

	Returns a region JSON.
	"""
	url = '/location/regions/%s' % str(regionId)
	return client._request(url, Request.GET)

def get_country(client, countryId):
	"""
	:param client: the CultureMesh API client
	:param eventId: the if of the country to fetch

	Returns a country JSON.
	"""
	url = '/location/countries/%s' % str(countryId)
	return client._request(url, Request.GET)

def location_autocomplete(client, input_text):
	"""
	:param client: the CultureMesh API client
	:param input_text: partial input text to a query field

	Returns a list of location JSONs
	in order of relevance.
	"""
	query_params = {'input_text': input_text}
	url = '/location/autocomplete'
	return client._request(url, Request.GET, query_params=query_params)