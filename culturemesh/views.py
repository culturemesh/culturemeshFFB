from flask import render_template, request
from culturemesh import app
from culturemesh.client import Client

import hashlib
import http.client as httplib
import requests
import config

from .forms import SearchForm


@app.route("/")
@app.route("/index")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')

@app.route("/register")
def render_register_page():
	return render_template('register.html')

#TODO: make this work?
@app.route("/register", methods=['POST'])
def register():
	name = request.form["name"]
	email = request.form["email"]
	password = request.form["password"]
	confirm_password = request.form["confirm-password"]
	user_string = "Name: " + name + " Email: " + email + " Password: " + " Confirm Password: " + confirm_password
	return render_template('dashboard.html', user=user_string)

@app.route("/login")
def render_login_page():
	return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	email = request.form["email"]
	password = request.form["password"]
	return "Email: " + email + " Password: " + password

@app.route("/search", methods=['GET', 'POST'])
def render_search_page():
	if request.method == 'POST':
		c = Client(mock=True)
		data = request.form
		networks = c.get_networks(10, max_id=None) # filter_=data)
		return render_template('search_results.html', networks=networks)
	else:
		form = SearchForm()
		return render_template('search.html', form=form)

@app.route("/home")
@app.route("/home/dashboard")
def render_user_home():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	return render_template('home_dashboard.html', user=user)

@app.route("/home/account")
def render_user_home_account():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")
	return render_template('home_account.html', user=user)

@app.route("/home/events")
def render_user_home_events():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	# TODO: incorporate paging into the events hosting API call
	events_hosting = c.get_user_events(user_id, "hosting", 5)
	if events_hosting is None:
		return page_not_found("")

	return render_template('home_events.html', user=user,
		events_hosting=events_hosting)

@app.route("/home/networks")
def render_user_home_networks():
	user_id = int(request.args.get('id'))
	c = Client(mock=True)
	user = c.get_user(user_id)

	if user is None:
		return page_not_found("")

	# TODO: incorporate paging into the user networks call.
	user_networks = c.get_user_networks(user_id, count=5)
	# TODO: construct network titles

	titles = []
	for network in user_networks:
		title_template = "From %s, %s, %s in %s, %s, %s, that speak %s."
		location_cur = network['location_cur']
		city = c.get_city(location_cur['city_id'])['name']
		region = c.get_region(location_cur['region_id'])['name']
		country = c.get_country(location_cur['country_id'])['name']

		location_origin = network['location_origin']
		city_orig = c.get_city(location_origin['city_id'])['name']
		region_orig = c.get_region(location_origin['region_id'])['name']
		country_orig = c.get_country(location_origin['country_id'])['name']



		language = network['language_origin']['name']
		titles.append(title_template % (city_orig.title(), region_orig.title(), country_orig.title(),
															      city.title(), region.title(), country.title(), language))

	return render_template('home_networks.html', user=user,
		user_network_titles=titles)

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
