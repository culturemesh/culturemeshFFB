#
# Tests client/posts.py
# 

from nose.tools import assert_true
from culturemesh.client import Client

def test_posts():
	c = Client(mock=True)

	post = c.get_post(4)
	print(post)
	assert_true(post['vid_link'] == "https://www.lorempixel.com/1016/295")

# TODO: do more