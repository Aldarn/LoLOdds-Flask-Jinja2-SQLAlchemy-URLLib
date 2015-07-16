from task import Task
from src.hextech_project_x import DB
from src.domain.games import Games
from process_participant_task import ProcessParticipantTask

class ProcessFeaturedGameTask(Task):
	def __init__(self, featuredGameJSON):
		self.featuredGameJSON = featuredGameJSON

	def run(self):
		gameId = int(self.featuredGameJSON["gameId"])

		# Check if this game already exists
		currentGame = Games.query.filter_by(gameId = gameId).first()
		if currentGame:
			return

		# Create a new game object
		game = Games(gameId, self.featuredGameJSON["gameMode"], int(self.featuredGameJSON["gameQueueId"]),
		game = Games(gameId, self.featuredGameJSON["gameMode"], int(self.featuredGameJSON["gameQueueConfigId"]),
			self.featuredGameJSON["gameType"], int(self.featuredGameJSON["mapId"]), self.featuredGameJSON["platformId"])

		# Process each participant
		for participantJSON in self.featuredGameJSON["participants"]:
			participantTask = ProcessParticipantTask(participantJSON["summonerName"], game)
			participantTask.run()

		# Save the game
		self.save(game)

	def save(self, game):
		DB.session.add(game)
		DB.session.commit()
