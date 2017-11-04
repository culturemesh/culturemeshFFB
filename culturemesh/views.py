from flask import render_template, request
from culturemesh import app

import hashlib
import http.client as httplib
import requests

@app.route("/example_api_call")
def example_api_call():
	# This will be replaced by an API call.  i.e. "http://www.culturemesh.com/api/v1/user?id=734"
	r = requests.get("http://www.gutenberg.org/cache/epub/345/pg345.txt")
	return render_template('example.html', example=r.text)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')
##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
