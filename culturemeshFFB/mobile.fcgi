#!/home/culturp7/python/bin/python3.6

# Load environment variables.
exec(open('.profile.py').read())

from flup.server.fcgi import WSGIServer
from run import app

from flask_sslify import SSLify

SSLify(app)
WSGIServer(app).run()
