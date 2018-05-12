#
# CultureMesh Posts API
#

from .client import Request

####################### GET methods #######################

def ping_post(client):
    url = '/post/ping'
    return client._request(url, Request.GET)

def get_post(client, postId):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to retrieve.

	Returns the corresponding post JSON.
	"""

	url = '/post/%s' % str(postId)
	return client._request(url, Request.GET)

def get_post_replies(client, postId, count, max_id=None):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to fetch replies from
	:param count: the number of results to return (may return less)
	:param max_id: the maximum id, inclusive, of post replies to fetch

	Returns a list of postReply JSONs, in reverse sorted order by
	id.
	"""
	url = '/post/%s/replies' % str(postId)
	query_params = {'count': count}
	if max_id is not None:
		query_params['max_id'] = max_id
	return client._request(url, Request.GET, query_params=query_params)

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
