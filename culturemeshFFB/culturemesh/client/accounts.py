#
# CultureMesh Accounts API
#

from .client import Request
####################### GET methods #######################

def get_token(client, email_or_username, password):
	"""
	Returns an authentication token for this user/email and password
	combination. This token is meant to live as long as the user's session,
	and available in login-required views.

	:param client: the CultureMesh API Client
	:param email_or_username: The email or username of the user
	:param password: The password of the user
	"""
	url = 'account/token'
	basic_auth = (email_or_username, password)
	return client._request(url, Request.GET, basic_auth=basic_auth)
