#!/usr/bin/env/python2.7

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from src.services.game_odds_service import GAME_ODDS_SERVICE
import json

# Create our web server - too easy
APP = Flask(__name__)

# Load the config
APP.config.from_object('src.resources.client_config')

# Create a DB handle from the app
DB = SQLAlchemy(APP)

@APP.route('/')
def index():
    # TODO: This should be exposed via an API endpoint and loaded with AJAX
    currentGameOdds = GAME_ODDS_SERVICE.getGamesWithOdds()

    # Render the template with the current game odds
    return render_template('index.html', currentGameOdds = currentGameOdds)

if __name__ == '__main__':
    APP.run(debug = True)
