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

		# Check if these stats have already been recorded
		with DB.session.no_autoflush:
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
		summonerChampionStats = SummonerChampionStats(self.summoner.summonerId, championId,
			self.championJSON["stats"]["totalSessionsWon"], self.championJSON["stats"]["totalSessionsLost"])

		DB.session.add(summonerChampionStats)
		self.summoner.summonerChampionStats.append(summonerChampionStats)

	"""
	Updates an existing entry.
	"""
	def updateExistingChampionStats(self, currentChampionStats):
		currentChampionStats.totalSessionsWon = self.championJSON["stats"]["totalSessionsWon"]
		currentChampionStats.totalSessionsLost = self.championJSON["stats"]["totalSessionsLost"]
