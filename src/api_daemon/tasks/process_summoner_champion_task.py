from task import Task
from src.hextech_project_x import DB
from src.domain.summoner_champion_stats import SummonerChampionStats
from sqlalchemy import and_

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
		currentChampionStats = SummonerChampionStats.query.filter_by(
			and_(summonerId = self.summoner.summonerId, championId = championId)).first()

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
			self.championJSON["totalSessionsWon"], self.championJSON["totalSessionsLost"])

		self.summoner.children.append(summonerChampionStats)
		DB.session.add(summonerChampionStats)
		DB.session.commit()

	"""
	Updates an existing entry.
	"""
	def updateExistingChampionStats(self, currentChampionStats):
		currentChampionStats.totalSessionsWon = self.championJSON["totalSessionsWon"]
		currentChampionStats.totalSessionsLost = self.championJSON["totalSessionsLost"]
		DB.session.commit()
