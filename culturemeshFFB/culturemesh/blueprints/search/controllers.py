from flask import Blueprint, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFError
from culturemesh.client import Client
from culturemesh.blueprints.search.forms.search_forms import SearchForm
from culturemesh.blueprints.search.forms.search_forms import GoToNetworkForm
from culturemesh.utils import populate_network_with_location_names

from http import HTTPStatus

from culturemesh.blueprints.search.utils import get_no_search_results_msg
from culturemesh.blueprints.search.utils import prepare_location_for_search
from culturemesh.blueprints.search.utils import get_location_population
from culturemesh.blueprints.search.constants import GO_TO_NETWORK_MAX_RETRIES
from culturemesh.blueprints.search.constants import GO_TO_NETWORK_WAIT_SECS

import time

search = Blueprint('search', __name__, template_folder='templates')

MAX_SUGGESTIONS = 10

@search.route("/", methods=['GET', 'POST'])
def render_search_page():

    if request.method == "GET":
        return render_template('search.html', form=SearchForm())

    # POST
    c = Client(mock=False)
    data = request.form

    if not SearchForm(data).validate():
        return render_template(
            'search.html',
            form=SearchForm(),
            msg="Could not process your search.  Did you leave a field blank?"
        )

    search_type = str(data.get('search_type'))

    language = None
    from_location = None

    if search_type == "location":
        from_location = data['origin_or_language']
        network_type_suggestions = c.location_autocomplete(from_location)
    elif search_type == "language":
        language = data['origin_or_language']
        network_type_suggestions = c.language_autocomplete(language)
    else:
        raise Exception("Invalid Search Type %s" % search_type)

    near_location = data['residence']
    current_location_suggestions = c.location_autocomplete(near_location)

    # Where there some suggestions?  If not tell the user.
    if not network_type_suggestions or not current_location_suggestions:
        msg = get_no_search_results_msg(
            search_type,
            network_type_suggestions,
            current_location_suggestions,
            data['origin_or_language'],
            data['residence']
        )

        return render_template(
            'search.html', form=SearchForm(), msg=msg
        )

    network_type_suggestions = network_type_suggestions[:min(
        MAX_SUGGESTIONS, len(network_type_suggestions)
    )]

    current_location_suggestions = current_location_suggestions[:min(
        MAX_SUGGESTIONS, len(current_location_suggestions)
    )]

    if search_type == "location":
        for s in network_type_suggestions:
            prepare_location_for_search(c, s)

        network_type_suggestions = sorted(
            network_type_suggestions,
            key=lambda x: get_location_population(x),
            reverse=True
        )

    for s in current_location_suggestions:
        prepare_location_for_search(c, s)

    current_location_suggestions = sorted(
        current_location_suggestions,
        key=lambda x: get_location_population(x),
        reverse=True
    )

    if search_type == "location":

        return render_template(
            'location_suggestions.html',
            location_suggestions=network_type_suggestions,
            current_location_suggestions=current_location_suggestions,
            form=GoToNetworkForm()
        )
    elif search_type == "language":
        return render_template(
            'language_suggestions.html',
            language_suggestions=network_type_suggestions,
            current_location_suggestions=current_location_suggestions,
            form=GoToNetworkForm()
        )
    else:
        raise Exception("Invalid Search Type %s" % search_type)


@search.route("/gotonetwork/", methods=['POST'])
def go_to_network(tries=0):

    c = Client(mock=False)
    form = GoToNetworkForm(request.form)
    if not form.validate():
        raise CSRFError()

    curr_loc_query = request.form['curr_loc']

    try:
        if request.form.get('language', None):
            networks = c.get_networks(
                1, near_location=curr_loc_query, language=request.form['language']
            )
        elif request.form.get('from_loc', None):
            networks = c.get_networks(
                1, near_location=curr_loc_query, from_location=request.form['from_loc']
            )
        else:
            abort(HTTPStatus.BAD_REQUEST)
    except requests.exceptions.ConnectionError as e:

        # Let's keep trying, but less agressively.
        if tries >= GO_TO_NETWORK_MAX_RETRIES:
            raise e
        time.sleep(GO_TO_NETWORK_WAIT_SECS)
        go_to_network(tries + 1)

    if len(networks) != 1:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)

    return redirect(url_for('networks.network', id=str(networks[0]['id'])))
