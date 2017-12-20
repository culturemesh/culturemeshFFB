#
# Tests client/users.py
# 

from nose.tools import assert_true, assert_equal
from culturemesh.client import Client

def test_get_user():
	"""
	Tests we can retrieve a user.  For illustrative purposes, the client is not mocked!
	"""

	c = Client(mock=True)

	# Here, we want to mock the client. 
	
	user = c.get_user(3)
	print(user)
	assert_true(user is not None)

def test_get_users():
	"""
	Tests we can retrieve all users. For illustrative purposes, client returns mock
	data. 
	"""
	c = Client(mock=True)
	users = c.get_users()
	print(users)

	assert_equal(len(users), 5)

def test_get_posts():
	"""
	Tests we can retrieve posts for a user. For illustrative purposes, client returns mock
	data. 
	"""
	c = Client(mock=True)
	posts = c.get_user_posts(userId=4)
	print(posts)

	assert_equal(len(posts), 2)

def test_get_events():
	"""
	Tests we can retrieve events related to a user. For illustrative purposes, client returns mock
	data. 
	"""
	c = Client(mock=True)
	events = c.get_user_events(userId=5, role="hosting")
	print(events)

	assert_equal(len(events), 2)
	assert_equal(len(c.get_user_events(userId=1, role="hosting")), 0)