from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

import os

app = Flask(__name__,
            template_folder="templates")

# Install Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Install CSRF Protection
app.secret_key = str(os.environ['WTF_CSRF_SECRET_KEY'])
csrf = CSRFProtect(app)

import culturemesh.views

# Register Blueprints

from culturemesh.blueprints.user_home.controllers import user_home
from culturemesh.blueprints.search.controllers import search
from culturemesh.blueprints.networks.controllers import networks
from culturemesh.blueprints.events.controllers import events
from culturemesh.blueprints.posts.controllers import posts
from culturemesh.blueprints.users.controllers import users
from culturemesh.blueprints.dev.controllers import dev

app.register_blueprint(user_home, url_prefix='/home')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(networks, url_prefix='/network')
app.register_blueprint(events, url_prefix='/event')
app.register_blueprint(posts, url_prefix='/post')
app.register_blueprint(users, url_prefix='/u')
app.register_blueprint(dev, url_prefix='/dev')
