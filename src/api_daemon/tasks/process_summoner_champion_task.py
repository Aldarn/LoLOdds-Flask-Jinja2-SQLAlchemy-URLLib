from task import Task
from src.hextech_project_x import DB
from src.domain.summoner_champion_stats import SummonerChampionStats

class ProcessSummonerChampionTask(Task):
	def __init__(self, championJSON, summoner):
		self.championJSON = championJSON
		self.summoner = summoner

	"""
	Checks for an existing entry acts accordingly.
	"""
	def run(self):
		championId = int(self.championJSON["id"])

		print "championId %s" % championId
		print "championJSON %s" % self.championJSON

		# Check if these stats have already been recorded
		currentChampionStats = SummonerChampionStats.query.filter_by(summonerId = self.summoner.summonerId,
			championId = championId).first()

		# Update the existing one
		if currentChampionStats:
			self.updateExistingChampionStats(currentChampionStats)
		else:
			self.save(championId)

	"""
	Saves a new entry.
	"""
	def save(self, championId):
		# TODO: Get the champion image url
		championImageUrl = "TODO"

		summonerChampionStats = SummonerChampionStats(self.summoner.summonerId, championId, championImageUrl,
			self.championJSON["stats"]["totalSessionsWon"], self.championJSON["stats"]["totalSessionsLost"])

		self.summoner.summonerChampionStats.append(summonerChampionStats)
		DB.session.add(summonerChampionStats)
		DB.session.commit()

	"""
	Updates an existing entry.
	"""
	def updateExistingChampionStats(self, currentChampionStats):
		currentChampionStats.totalSessionsWon = self.championJSON["stats"]["totalSessionsWon"]
		currentChampionStats.totalSessionsLost = self.championJSON["stats"]["totalSessionsLost"]
		DB.session.commit()
