#
# Tests client/locations.py
#

from nose.tools import assert_true, assert_equal
import test.unit.client.client_test_prep
from culturemesh.client import Client

def test_get_city():
  """
  Basic get city API routine.
  """
  c = Client(mock=True)
  city1 = c.get_city(2)
  city2 = c.get_city(4)
  city3 = c.get_city(0)

  assert_true(city1 is not None)
  assert_equal(city1['name'], "City B")
  assert_equal(city1['population'], 100000)

  assert_true(city2 is not None)
  assert_equal(city2['name'], "City D")
  assert_equal(city2['population'], 280)
  print(city2)

  assert_true(city3 is None)


def test_get_region():
  """
  Basic get region API routine.
  """
  c = Client(mock=True)
  region1 = c.get_region(2)
  region2 = c.get_region(5)

  assert_true(region1 is not None)
  assert_equal(region1['name'], "south")
  assert_equal(region1['country_name'], 'corneria')
  print(region1)

  assert_true(region2 is None)

def test_get_country():
  """
  Basic get country API routine.
  """
  c = Client(mock=True)
  country1 = c.get_country(2)
  country2 = c.get_country(5)

  assert_true(country1 is not None)
  assert_equal(country1['name'], "rohan")
  print(country1)

  assert_equal(country1['latitude'], 100.100)

  assert_true(country2 is None)

def test_autocomplete():
  """
  Test mock autocomplete.
  """
  c = Client(mock=True)
  autocomplete_ = c.location_autocomplete("some text")
  print(autocomplete_)
