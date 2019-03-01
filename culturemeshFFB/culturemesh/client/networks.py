#
# CultureMesh Networks API
#

from .client import Request

####################### GET methods #######################

def ping_network(client):
    url = 'network/ping'
    return client._request(url, Request.GET)

def get_networks(client,
                 count,
                 max_id=None,
                 near_location=None,
                 from_location=None,
                 language=None):
    """
    :param client: the CultureMesh API client
    :param near_location: A comma-separated list of country_id,
                          region_id, and city_id, in that order.
    :param from_location: A comma-separated list of country_id,
                          region_id, and city_id, in that order.
    :param language: Name of language.

    Returns a list of networks filtered by FILTER.
    """
    query_params = {'count': count}
    if max_id:
        query_params['max_id'] = max_id

    if near_location:
        near_location = near_location.replace('null', '-1')
        query_params['near_location'] = near_location

    if from_location:
        from_location = from_location.replace('null', '-1')
        query_params['from_location'] = from_location

    if language:
        query_params['language'] = language

    url = 'network/networks'
    return client._request(url, Request.GET, query_params=query_params)


def get_network(client, networkId):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return.

    Returns JSON of network.
    """
    url = 'network/%s' % str(networkId)
    return client._request(url, Request.GET)


def get_network_posts(client, networkId, count, max_id=None):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network to return a list of posts for.

    Returns list of posts JSONs for posts in networkId
    """
    url = 'network/%s/posts' % str(networkId)
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
    url = 'network/%s/events' % str(networkId)
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
    url = 'network/%s/users' % str(networkId)
    query_params = {'count': count}
    if max_id is not None:
        query_params['max_id'] = max_id
    return client._request(url, Request.GET, query_params=query_params)

def get_network_user_count(client, networkId):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network

    Returns the number of users on this network.
    """
    url = 'network/%s/user_count' % str(networkId)
    return client._request(url, Request.GET)

def get_network_post_count(client, networkId):
    """
    :param client: the CultureMesh API client
    :param networkId: The id of the network

    Returns the number of posts on this network.
    """
    url = 'network/%s/post_count' % str(networkId)
    return client._request(url, Request.GET)

####################### POST methods #######################
####################### PUT methods #######################
