#!/usr/bin/env/python2.7

# Fix for PEP0366 - https://www.python.org/dev/peps/pep-0366/
# Essentially, if a PYTHONPATH environment variable has not been set, and a 
# main module (i.e this script) uses package level imports, the package 
# base directory must be added to sys.path for Python to locate the package 
# imports. It must also have its __package__ set, which has already been done 
# in the entry point at the end of this script.
import sys
import os
sys.path.append('%s/../../' % os.path.dirname(__file__))

import time
from src.api.featured_games.featured_games import FEATURED_GAMES
from tasks.process_featured_game_task import ProcessFeaturedGameTask

def run():
	# Run indefinitely, supervisor manages the state for us
	while True:
		# Grab the current featured games JSON
		# TODO: This should be a task ran asynchronously via Celery (RabbitMQ wrapper) or equivalent
		success, featuredGamesJSON = FEATURED_GAMES.getFeaturedGames()

		# If the call fails set a smaller interval
		if not success:
			# TODO: Log this properly
			print "Failed to get featured games, got: %s" % featuredGamesJSON
			clientRefreshInterval = 1
		else:
			print "getting featured games"

			if len(featuredGamesJSON["gameList"]) == 0:
				print "received empty game list, sleeping..."
				clientRefreshInterval = 1

			else:
				# Set the client refresh interval
				clientRefreshInterval = featuredGamesJSON["clientRefreshInterval"]

				print "got featured games, refresh interval: %s" % clientRefreshInterval

				# Create and run the tasks to process each game
				# TODO: Again, this should be a proper queued async task
				for gameJSON in featuredGamesJSON["gameList"]:
					featuredGameTask = ProcessFeaturedGameTask(gameJSON)
					featuredGameTask.run()

				print "featured games stored, sleeping"

		# Wait the recommended length of time until we process new things
		time.sleep(clientRefreshInterval)

if __name__ == "__main__" and __package__ is None:
	__package__ = "src.api_daemon.daemon"
	run()
