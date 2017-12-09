#
# CultureMesh Posts API
#

####################### GET methods #######################

from .client import Request

def get_post(client, postId):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to retrieve. 

	Returns the corresponding post JSON.
	"""

	url = '/post/%s' % str(postId)
	return client._request(url, Request.GET)

def get_post_replies(client, postId):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to fetch replies from

	Returns a list of postReply JSONs.
	"""
	raise NotImplementedError

####################### POST methods #######################

def create_post(client, post):
	"""
	:param client: the CultureMesh API client
	:param post: JSON of post to create.

	Creates a new post.
	"""
	raise NotImplementedError

def create_post_reply(client, postId, reply):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to reply to
	:param reply: JSON of the reply to post

	Posts a reply to a post by ID.
	"""
	raise NotImplementedError