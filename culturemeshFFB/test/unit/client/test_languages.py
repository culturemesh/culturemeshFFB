#
# Tests client/languages.py
#

from nose.tools import assert_true, assert_equal
import test.unit.client.client_test_prep
from culturemesh.client import Client

def test_language():
  """
  Basic functionality of retrieving
  a mock language.
  """

  c = Client(mock=True)
  lang1 = c.get_language(2)
  print(lang1)
  assert_true(lang1)
  assert_equal(lang1['name'], "entish")

def test_autocomplete():
  """
  Basic mock autocomplete functionality.
  """

  c = Client(mock=True)
  autocomplete_ = c.language_autocomplete("some text")
  print(autocomplete_)
  assert_equal(autocomplete_, "some text + [language autocompleted text]")
