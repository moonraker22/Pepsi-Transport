from flask import Flask

# from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

# Set FLASK_ENV=development or FLASK_ENV=production
if app.config["ENV"] == "production":
    app.config.from_object("config.Production")

elif app.config["ENV"] == "testing":
    app.config.from_object("config.Testing")
else:
    app.config["ENV"] == "development"
    app.config.from_object("config.Development")

# Flask toolbar
# toolbar = DebugToolbarExtension(app)

# DB instatiation
db = SQLAlchemy(app)
db.app = app

# Login mgr instatiation
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must log in to view this page"
login_manager.login_message_category = "red accent-1"


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


import knz_kustomz.views
