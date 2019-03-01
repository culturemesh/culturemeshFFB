#
# Tests client/users.py
#

from nose.tools import assert_true, assert_equal
import test.unit.client.client_test_prep
from culturemesh.client import Client

def test_get_user():
	"""
	Tests we can retrieve a user.  The client returns dummy data.
	"""

	c = Client(mock=True)

	# Here, we want to mock the client.

	user = c.get_user(3)
	print(user)
	assert_true(user is not None)

def test_get_users():
	"""
	Tests basic user pagination.
	"""
	c = Client(mock=True)

	users1 = c.get_users(3)
	assert_equal(len(users1), 3)
	assert_equal(users1[0]['id'], 5)

	min_id_got = min(u['id'] for u in users1)

	users2 = c.get_users(3, max_id=min_id_got - 1)
	assert_equal(len(users2), 2)
	assert_equal(users2[0]['id'], 2)

	users3 = c.get_users(3, 1)
	assert_equal(len(users3), 1)

def test_get_posts():
	"""
	Tests user posts with paginated calls. The client returns dummy data.
	"""
	c = Client(mock=True)
	posts = c.get_user_posts(user_id=4, count=2)
	print(posts)
	assert_equal(len(posts), 2)

	posts2 = c.get_user_posts(user_id=4, count=2, max_id=2)
	print(posts2)
	assert_equal(len(posts2), 1)

	posts = c.get_user_posts(user_id=4, count=1)
	print(posts)
	assert_equal(len(posts), 1)
	assert_equal(posts[0]['id'], 5)

def test_get_events():
	"""
	Tests we can retrieve events related to a user.
	The client returns dummy data.
	"""
	c = Client(mock=True)
	events = c.get_user_events(user_id=5, role="hosting", count=3)
	print(events)
	assert_equal(len(events), 2)
	assert_true(events[0]['id'] > events[1]['id'])

	events1 = c.get_user_events(user_id=5, role="hosting", count=2, max_id=3)
	assert_equal(len(events1), 1)

	assert_equal(len(c.get_user_events(user_id=1, role="hosting", count=5)), 0)

def test_get_networks():
	"""
	Tests we can retrieve mock networks to which a user belongs.
	The client returns dummy data.
	"""
	c = Client(mock=True)
	user_id = 4;
	networks = c.get_user_networks(user_id=user_id, count=3)
	print(networks)
	assert_equal(networks[0]['id'], 2)
	assert_equal(networks[1]['id'], 1)

	networks = c.get_user_networks(
		user_id=user_id, count=3, max_register_date="2017-02-25 11:53:30"
	)
	assert_equal(len(networks), 1)
	assert_equal(networks[0]['id'], 1)

	networks = c.get_user_networks(user_id=user_id, count=1)
	assert_equal(len(networks), 1)
	assert_equal(networks[0]['id'], 2)

