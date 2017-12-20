#
# Tests client/posts.py
# 

from nose.tools import assert_true, assert_equal
from culturemesh.client import Client

def test_get_post():
  """
  Tests we can get a single post.
  """
  c = Client(mock=True)

  post = c.get_post(4)
  print(post)
  assert_equal(post['vid_link'], "https://www.lorempixel.com/1016/295")

def test_get_post_replies():
  """
  Tests that we can get post replies as expected. 
  """
  c = Client(mock=True)
  posts1 = c.get_post_replies(1)
  posts2 = c.get_post_replies(2)
  print(posts1)

  assert_equal(len(posts1), 2)
  assert_equal(len(posts2), 0)