#
# Tests client/networks.py
#

from nose.tools import assert_true, assert_equal
import test.unit.client.client_test_prep
from culturemesh.client import Client


def test_get_networks():
    """
    Tests basic network retrieval pagination. For illustrative purposes,
    client returns mock data.
    """
    c = Client(mock=True)
    networks = c.get_networks(10)
    assert_equal(len(networks), 2)

    networks1 = c.get_networks(1)
    assert_equal(networks1[0]['id'], 2)
    assert_equal(len(networks1), 1)

    networks2 = c.get_networks(1, max_id=1)
    assert_equal(networks2[0]['id'], 1)
    assert_equal(len(networks2), 1)


def test_get_network():
    """
    Tests we can retrieve a network. For illustrative purposes, client
    returns mock data.
    """
    c = Client(mock=True)
    network = c.get_network(1)
    assert_true(network is not None)


def test_get_network_posts():
    """
    Tests we can retrieve a network's posts. For illustrative purposes,
    client returns mock data.
    """
    c = Client(mock=True)
    posts = c.get_network_posts(2, 10)
    assert_true(len(posts) == 3)

    posts1 = c.get_network_posts(2, 1)
    assert_equal(posts1[0]['id'], 4)
    assert_equal(len(posts1), 1)

    posts2 = c.get_network_posts(2, 1, max_id=3)
    assert_equal(posts2[0]['id'], 2)
    assert_equal(len(posts2), 1)


def test_get_network_events():
    """
    Tests we can retrieve a network's events. For illustrative purposes,
    client returns mock data.
    """
    c = Client(mock=True)
    events = c.get_network_events(1, 10)
    assert_true(len(events) == 2)

    events1 = c.get_network_events(1, 1)
    assert_equal(events1[0]['id'], 3)
    assert_equal(len(events1), 1)

    events2 = c.get_network_events(1, 1, max_id=3)
    assert_equal(events2[0]['id'], 3)
    assert_equal(len(events2), 1)


def test_get_network_users():
    """
    Tests we can retrieve a network's users (network registrations).
    For illustrative purposes, client returns mock data.
    """
    c = Client(mock=True)
    registrations = c.get_network_users(2, 10)
    assert_true(len(registrations) == 3)

    registrations1 = c.get_network_users(2, 1)
    assert_equal(registrations1[0]['join_date'], "2017-02-27 11:53:30")
    assert_equal(len(registrations1), 1)

    registrations2 = c.get_network_users(2, 1, max_id="2017-02-28 11:53:30")
    assert_equal(registrations2[0]['join_date'], "2017-02-27 11:53:30")
    assert_equal(len(registrations2), 1)
