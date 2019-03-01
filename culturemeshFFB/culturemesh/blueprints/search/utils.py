"""
Contains utility routines for the search page.
"""

def get_location_population(location):
    city, region, country = location['full']
    if city:
        return city['population']
    if region:
        return region['population']
    if country:
        return country['population']
    return -1

def prepare_location_for_search(client, location):
    """
    Takes a location as returned by a call to location autocomplete,
    and populates it with its name, its query parameter for future API
    calls, and adds to it the full data structure from the API.

    :param client: A culturemesh API client instance.
    :param location: The dictionary to be populated for search.
    """
    city_id = location['city_id']
    region_id = location['region_id']
    country_id = location['country_id']

    city = None
    region = None
    country = None

    city_name = None
    region_name = None
    country_name = None

    if city_id and city_id != 'null':
        city = client.get_city(city_id)
        city_name = city['name']
    else:
        city_id = '-1'

    if region_id and region_id != 'null':
        region = client.get_region(region_id)
        region_name = region['name']
    else:
        region_id = '-1'

    if country_id and country_id != 'null':
        country = client.get_country(country_id)
        country_name = country['name']
    else:
        country_id = '-1'

    name = ', '.join(
        [l for l in [city_name, region_name, country_name] if l]
    )

    query = ','.join([str(i) for i in [country_id, region_id, city_id]])

    location['name'] = name
    location['query'] = query
    location['full'] = [city, region, country]

def get_no_search_results_msg(search_type,
                              network_type_suggestions,
                              current_location_suggestions,
                              network_type_query,
                              current_location_query):

    if search_type not in ['location', 'language']:
        raise ValueError

    if network_type_suggestions and current_location_suggestions:
        raise ValueError

    msg = "Your search for \"%s\" did not match any results. \
           Make sure you spelled things correctly, or try another \
           language/location."

    if not network_type_suggestions and not current_location_suggestions:
        if search_type == 'location':
            sub_msg = "people from %s in %s"
        else:
            sub_msg = "people who speak %s in %s"
        msg = msg % (sub_msg % (network_type_query, current_location_query))
    elif not network_type_suggestions:
        if search_type == 'location':
            sub_msg = "people from %s"
        else:
            sub_msg = "people who speak %s"
        msg = msg % (sub_msg % (network_type_query))
    elif not current_location_suggestions:
        sub_msg = "people in %s"
        msg = msg % (sub_msg % (current_location_query))

    return msg
