from flask import Blueprint
from database import mysql

dbdiagnostics = Blueprint("dbdiagnostics", __name__)

@dbdiagnostics.route("/showtables")
def get():
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	return "tablenames: " + str(tablenames)

@dbdiagnostics.route("/retrieve_tables_and_columns")
def retrieve_tables_and_columns():
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	complete_list = ""
	for i in xrange(len(tablenames)):
		cur_table = str(tablenames[i]).split("'")[1]
		complete_list += cur_table
		complete_list += ": "
		#cursor = mysql.connect().cursor()
		cursor.execute("DESCRIBE " + cur_table)
		cur_table_columns = cursor.fetchall()
		for j in cur_table_columns:
			complete_list += str(j[0]) + ", "
		complete_list += "<br \\><br \\>"
	return complete_list

@dbdiagnostics.route("/sql")
def sql():
	cursor = mysql.connect().cursor()
	cmd = request.args.get("command")
	if cmd != None:
		cursor.execute(cmd) 
		return str(cursor.fetchall()) + '<br><br><form action="sql"><input type="text" name="command" placeholder="SQL command"></input></form>'
	else:
		return '<form action="sql"><input type="text" name="command" placeholder="SQL command"></input></form>'