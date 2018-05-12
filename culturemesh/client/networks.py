#
# CultureMesh Networks API
#

####################### GET methods #######################

from .client import Request

def ping_network(client):
    url = '/network/ping'
    return client._request(url, Request.GET)

def get_networks(client, count, max_id=None, filter_=None):
    """
    :param client: the CultureMesh API client
    :param filter: A json with which to filter a site-wide network query.

    Returns a list of networks filtered by FILTER.
    """
    params = {'filter': filter_}
    query_params = {'count': count}
    if max_id is not None:
        query_params['max_id'] = max_id
    url = '/networks'
    return client._request(url, Request.GET, body_params=params,
                           query_params=query_params)


def get_network(client, networkId):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return.

    Returns JSON of network.
    """
    url = '/network/%s' % str(networkId)
    return client._request(url, Request.GET)


def get_network_posts(client, networkId, count, max_id=None):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return a list of posts for.

    Returns list of posts JSONs for posts in networkId
    """
    url = '/network/%s/posts' % str(networkId)
    query_params = {'count': count}
    if max_id is not None:
        query_params['max_id'] = max_id
    return client._request(url, Request.GET, query_params=query_params)


def get_network_events(client, networkId, count, max_id=None):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return a list of events for.

    Returns list of events JSONs for events in networkId
    """
    url = '/network/%s/events' % str(networkId)
    query_params = {'count': count}
    if max_id is not None:
        query_params['max_id'] = max_id
    return client._request(url, Request.GET, query_params=query_params)


def get_network_users(client, networkId, count, max_id=None):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return a list of network
    registrations for.

    Returns list of Network Registration JSONs for networkId
    """
    url = '/network/%s/users' % str(networkId)
    query_params = {'count': count}
    if max_id is not None:
        query_params['max_id'] = max_id
    return client._request(url, Request.GET, query_params=query_params)

####################### POST methods #######################
####################### PUT methods #######################
