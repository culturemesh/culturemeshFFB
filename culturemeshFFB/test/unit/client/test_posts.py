#
# Tests client/posts.py
#

from nose.tools import assert_true, assert_equal
import test.unit.client.client_test_prep
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
  posts1 = c.get_post_replies(1, count=5)
  posts2 = c.get_post_replies(2, count=5)
  print(posts1)

  posts3 = c.get_post_replies(1, count=1)
  posts4 = c.get_post_replies(1, count=3, max_id=1)

  assert_equal(len(posts1), 2)
  assert_equal(len(posts2), 0)
  assert_equal(len(posts3), 1)
  assert_equal(posts3[0]['id'], 2)
  assert_equal(len(posts4), 1)
  assert_equal(posts4[0]['id'], 1)
