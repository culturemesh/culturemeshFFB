from flask import Blueprint, request
from database import mysql

network = Blueprint("network", __name__)

@network.route("/search")
def search():
	from_location = request.args.get("from")
	in_location = request.args.get("in")
	cursor = mysql.connect().cursor()
	cursor.execute('select population, region_name, country_name from cities where name="' + from_location + '"')
	from_info = cursor.fetchall()
	cursor.execute('select population, region_name, country_name from cities where name="' + in_location + '"')
	in_info = cursor.fetchall()
	return from_location + ": " + str(from_info) + "<br>" + in_location + ": " + str(in_info)