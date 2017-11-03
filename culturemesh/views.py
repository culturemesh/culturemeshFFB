from flask import render_template, request
from database import mysql
from culturemesh import app

import hashlib
import httplib
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

@app.route("/select_users")
def select_users():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT id, username, first_name, last_name FROM users")
	users = cursor.fetchall()
	s = ""
	for u in users:
		s += str(u) + "<br \\>"
	return s

@app.route("/login", methods=['GET', 'POST'])
def login():
	email = request.form["emai[l"]
	password = request.form["password"]
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM users WHERE email = \'" + email + "\'")
	temp = cursor.fetchall()
	if temp != None:
		truePassword = str(temp)[3:len(temp) - 3]
		if hashlib.md5(password).hexdigest() == truePassword:
			return "Success!!!!! here is the main page"
			#return render_template('MainPage.html')
		else:
			return "Username or Password was incorrect. Try again."
	else:
		return "Username or Password was incorrect. Try again."

##################### Error handling #########################

@app.errorhandler(httplib.NOT_FOUND)
def page_not_found(e):
    return render_template('404.html'), httplib.NOT_FOUND

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return render_template('500.html'), httplib.INTERNAL_SERVER_ERROR
