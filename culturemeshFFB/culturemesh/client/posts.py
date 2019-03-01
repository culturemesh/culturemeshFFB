#
# CultureMesh Posts API
#
from .client import Request

####################### GET methods #######################

def ping_post(client):
    url = 'post/ping'
    return client._request(url, Request.GET)

def get_post(client, postId):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to retrieve.

	Returns the corresponding post JSON.
	"""

	url = 'post/%s' % str(postId)
	return client._request(url, Request.GET)

def get_post_reply(client, replyId):
	"""
	:param client: the CultureMesh API client
	:param replyId: the id of the post reply to retrieve.

	Returns the requested post reply JSON.
	"""

	url = 'post/reply/%s' % str(replyId)
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
	url = 'post/%s/replies' % str(postId)
	query_params = {'count': count}
	if max_id is not None:
		query_params['max_id'] = max_id
	return client._request(url, Request.GET, query_params=query_params)

def get_post_reply_count(client, postId):
	"""
	:param client: the CultureMesh API client
	:param postId: the id of the post to fetch reply count for

	Returns a JSON with a single reply_count element.
	"""
	url = 'post/%s/reply_count' % str(postId)
	return client._request(url, Request.GET)

####################### POST methods #######################

def create_post(client, current_user, post):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param post: JSON of post to create.

	Creates a new post.
	"""
	url = 'post/new'
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.POST, json=post, basic_auth=basic_auth
	)

def create_post_reply(client, current_user, postId, reply):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param postId: the id of the post to reply to
	:param reply: JSON of the reply to post

	Posts a reply to a post by ID.
	"""
	url = 'post/%s/reply' % str(postId)
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.POST, json=reply, basic_auth=basic_auth
	)

####################### PUT methods #######################

def update_post(client, current_user, post):
	"""
    :param client: the CultureMesh API client
    :param current_user: The current user object
    :param post: JSON of post with updates.

    Updates a post.
	"""
	url = 'post/new'
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.PUT, json=post, basic_auth=basic_auth
	)

def update_post_reply(client, current_user, postId, reply):
	"""
	:param client: the CultureMesh API client
	:param current_user: The current user object
	:param postId: the id of the parent post
	:param reply: JSON of the reply to update

	Update a post reply.
	"""
	url = 'post/%s/reply' % str(postId)
	basic_auth = (str(current_user.api_token), "")
	return client._request(
		url, Request.PUT, json=reply, basic_auth=basic_auth
	)
