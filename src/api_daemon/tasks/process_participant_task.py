from task import Task
from src.hextech_project_x import DB
from src.api.summoner.summoner_by_name import SUMMONER_BY_NAME
from src.api.stats.ranked_stats import RANKED_STATS
from src.domain.summoners import Summoners
from process_summoner_champion_task import ProcessSummonerChampionTask
from src.utils import getProfileIconUrl

class ProcessParticipantTask(Task):
	def __init__(self, participantName, game):
		self.participantName = participantName
		self.game = game

	"""
	Gets the summoner by the given participant name and processes its ranked stats if necessary.
	"""
	def run(self):
		# Get the existing summoner if it exists
		currentSummoner = Summoners.query.filter_by(name = self.participantName).first()

		# Grab the summoner data from their name
		success, summonerJSON = SUMMONER_BY_NAME.getSummoner(self.participantName)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner by name, got: %s" % summonerJSON
		else:
			# For brevity
			summonerJSON = summonerJSON[self.participantName]

			# Create the summoner object
			# Last stats modified and total wins / losses will be set by the champion with id 0 once we grab them shortly
			summonerId = int(summonerJSON["id"])
			summoner = Summoners(summonerId, summonerJSON["name"], getProfileIconUrl(summonerJSON["profileIconId"]),
				int(summonerJSON["revisionDate"]), 0, int(summonerJSON["summonerLevel"]), 0, 0)

			self.processRankedStats(currentSummoner, summoner)

	"""
	Gets the ranked stats for this summoner and updates them if they have changed, otherwise it updates
	the summoner if that has changed.
	"""
	def processRankedStats(self, summonerId, currentSummoner, summoner):
		# Get summoner champion ranked stats
		success, rankedStatsJSON = RANKED_STATS.getStats(summonerId)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner ranked stats JSON, got: %s" % rankedStatsJSON
		else:
			# Check if we need to update the stats
			lastStatsModified = rankedStatsJSON["modifyDate"]
			if not currentSummoner or lastStatsModified > currentSummoner.lastStatsModified:
				self.updateRankedStats(currentSummoner, summoner, lastStatsModified, rankedStatsJSON)

			# Update the existing object if it has changed
			elif summoner.lastModified > currentSummoner.lastModified:
				self.updateFromExistingSummoner(currentSummoner, summoner)

	def updateRankedStats(self, currentSummoner, summoner, lastStatsModified, rankedStatsJSON):
		# Save the modified date
		summoner.lastStatsModified = lastStatsModified

		# Update all the stats
		for championJSON in rankedStatsJSON["champions"]:
			if championJSON["id"] == 0:
				summoner.totalSessionsWon = championJSON["stats"]["totalSessionsWon"]
				summoner.totalSessionsLost = championJSON["stats"]["totalSessionsLost"]
			else:
				summonerChampionTask = ProcessSummonerChampionTask(championJSON, summoner)
				summonerChampionTask.run()

		# Commit the changes
		if currentSummoner:
			self.update(summoner)
		else:
			self.save(summoner, self.game)

	def save(self, summoner, game):
		game.children.append(summoner)
		DB.session.add(summoner)
		DB.session.commit()

	def update(self, summoner):
		DB.session.merge(summoner)
		DB.session.commit()

	def updateFromExistingSummoner(self, currentSummoner, summoner):
		summoner.totalSessionsWon = currentSummoner.totalSessionsWon
		summoner.totalSessionsLost = currentSummoner.totalSessionsLost

		self.update(summoner)