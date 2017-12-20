#
# Tests client/networks.py
#

from nose.tools import assert_true, assert_equal
from culturemesh.client import Client

def test_get_networks():
	"""
	Tests we can retrieve all networks. For illustrative purposes, client returns mock
	data.
	"""
	c = Client(mock=True)
	networks = c.get_networks()
	print(networks)

	assert_equal(len(networks), 2)
