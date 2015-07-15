#!/usr/bin/env/python2.7

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

# Create our web server - too easy
APP = Flask(__name__)

# Load the config
APP.config.from_object('src.resources.client_config')

# Create a DB handle from the app
DB = SQLAlchemy(APP)

@APP.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    APP.run(debug = True)
