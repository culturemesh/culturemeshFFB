#
# CultureMesh Languages API
#

from .client import Request

####################### GET methods #######################

def get_language(client, langId):
	"""
	:param client: the CultureMesh API client
	:param langId: the id of the language to fetch

	Returns a language JSON.
	"""
	url = '/language/%s' % str(langId)
	return client._request(url, Request.GET)

def language_autocomplete(client, input_text):
	"""
	:param client: the CultureMesh API client
	:param input_text: partial input text to a query field

	Returns a list of language JSONs
	in order of relevance.
	"""
	query_params = {'input_text': input_text}
	url = '/language/autocomplete'
	return client._request(url, Request.GET, query_params=query_params)
