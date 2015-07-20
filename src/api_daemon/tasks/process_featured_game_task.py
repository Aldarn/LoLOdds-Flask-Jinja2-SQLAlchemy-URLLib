from task import Task
from src.hextech_project_x import DB
from src.domain.games import Games
from process_participant_task import ProcessParticipantTask

class ProcessFeaturedGameTask(Task):
	def __init__(self, featuredGameJSON):
		self.featuredGameJSON = featuredGameJSON

	def run(self):
		gameId = int(self.featuredGameJSON["gameId"])

		print "gameId: %s" % gameId

		# Check if this game already exists
		currentGame = Games.query.filter_by(gameId = gameId).first()
		if currentGame:
			return

		print "game is new"

		# Create a new game object
		game = Games(gameId, self.featuredGameJSON["gameMode"], int(self.featuredGameJSON["gameQueueConfigId"]),
			self.featuredGameJSON["gameType"], int(self.featuredGameJSON["mapId"]), self.featuredGameJSON["platformId"])

		# Process each participant
		for participantJSON in self.featuredGameJSON["participants"]:

			summonerName = participantJSON["summonerName"]
			print "processing summoner %s" % summonerName

			participantTask = ProcessParticipantTask(summonerName, participantJSON["teamId"],
				participantJSON["championId"], game)
			participantTask.run()

		# Save the game
		self.save(game)

	"""
	Adds the game to the database and commits it all. Having the commit here and not in any
	of the other tasks ensures that only a complete game is committed to the database, rather
	than having partial data entered whilst other summoners are still being processed. This is
	useful as we don't need to add any handling on the client side to filter out partially
	processed data.
	"""
	def save(self, game):
		DB.session.add(game)
		DB.session.commit()
