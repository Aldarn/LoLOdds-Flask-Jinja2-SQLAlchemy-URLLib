#!/usr/bin/env/python2.7

import time
from src.api.featured_games.featured_games import FEATURED_GAMES
from tasks.process_featured_game_task import ProcessFeaturedGameTask

def run():
	clientRefreshInterval = 1

	# Run indefinitely, supervisor manages the state for us
	while True:
		# Grab the current featured games JSON
		# TODO: This should be a task ran asynchronously via Celery (RabbitMQ wrapper) or equivalent
		success, featuredGamesJSON = FEATURED_GAMES.getFeaturedGames()

		# If the call fails set a smaller interval
		if not success:
			clientRefreshInterval = 1
		else:
			# Set the client refresh interval
			clientRefreshInterval = featuredGamesJSON["clientRefreshInterval"]

			# Create and run the tasks to process each game
			# TODO: Again, this should be a proper queued async task
			for gameJSON in featuredGamesJSON["gameList"]:
				featuredGameTask = ProcessFeaturedGameTask(gameJSON)
				featuredGameTask.run()

		# Wait the recommended length of time until we process new things
		time.sleep(clientRefreshInterval)

if __name__ == '__main__':
	run()
