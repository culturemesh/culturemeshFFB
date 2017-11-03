from flask import Flask, render_template
from database import mysql
from network import network
from dbdiagnostics import dbdiagnostics

app = Flask(__name__)
import culturemesh.views

app.config['MYSQL_DATABASE_USER'] = 'culturp7_eric'
app.config['MYSQL_DATABASE_PASSWORD'] = 'culturemesh17'
app.config['MYSQL_DATABASE_DB'] = 'culturp7_rehearsal'
app.config['MYSQL_DATABASE_HOST'] = '50.116.65.175'
mysql.init_app(app)

app.register_blueprint(network)
app.register_blueprint(dbdiagnostics)
