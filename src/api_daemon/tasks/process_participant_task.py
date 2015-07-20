# -*- coding: utf-8 -*-

from task import Task
from src.hextech_project_x import DB
from src.api.summoner.summoner_by_name import SUMMONER_BY_NAME
from src.api.stats.ranked_stats import RANKED_STATS
from src.domain.game_summoners import GameSummoners
from src.domain.summoners import Summoners
from process_summoner_champion_task import ProcessSummonerChampionTask
from src.utils import getProfileIconUrl
from sqlalchemy.exc import OperationalError
from src.api.static.champion_by_id import CHAMPION_BY_ID
from src.utils import getChampionImageUrl

class ProcessParticipantTask(Task):
	def __init__(self, participantName, teamId, championId, game):
		self.participantName = participantName
		self.teamId = teamId
		self.championId = championId
		self.game = game

	"""
	Gets the summoner by the given participant name and processes its ranked stats if necessary.
	"""
	def run(self):
		# Grab the summoner data from their name
		success, summonerJSON = SUMMONER_BY_NAME.getSummoner(self.participantName)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner by name, got: %s" % summonerJSON
		else:
			print "got summoner %s" % summonerJSON

			# For brevity - get the dictionary for the summoner name (there's only ever one key which corresponds
			# to the summoner name)
			summonerJSON = summonerJSON[summonerJSON.keys()[0]]

			# Get the existing summoner if we have already stored it
			summoner = self.getExistingSummoner(int(summonerJSON["id"]))

			print "existing summoner: %s" % summoner

			# Update the existing summoner from the JSON
			if summoner:
				self._updateExistingSummoner(summoner, summonerJSON)

			# Create a new summoner from the JSON
			else:
				summoner = self.save(summonerJSON)

			# Process the ranked stats
			self.processRankedStats(summoner)

	"""
	Gets an existing summoner object from the database.
	"""
	def getExistingSummoner(self, summonerId):
		# Get the existing summoner if it exists
		try:
			with DB.session.no_autoflush:
				return Summoners.query.filter_by(summonerId = summonerId).first()
		except OperationalError, oe:
			print "Error loading current summoner: %s" % oe
		return None

	"""
	Creates a brand new summoner domain object.
	"""
	def save(self, summonerJSON):
		# Last stats modified and total wins / losses will be set by the champion with id 0 once we grab them shortly
		summoner = Summoners(int(summonerJSON["id"]), summonerJSON["name"], getProfileIconUrl(summonerJSON["profileIconId"]),
			int(summonerJSON["revisionDate"]), 0, int(summonerJSON["summonerLevel"]), 0, 0)

		DB.session.add(summoner)

		return summoner

	"""
	Updates an existing summoner object if necessary.
	"""
	def _updateExistingSummoner(self, summoner, summonerJSON):
		newLastModified = int(summonerJSON["revisionDate"])
		if newLastModified > summoner.lastModified:
			summoner.name = summonerJSON["name"]
			summoner.iconImageUrl = getProfileIconUrl(summonerJSON["profileIconId"])
			summoner.lastModified = newLastModified
			summoner.level = int(summonerJSON["summonerLevel"])

	"""
	Gets the ranked stats for this summoner.

	TODO: Consider moving this into a new "ProcessGameSummoner" task.
	"""
	def processRankedStats(self, summoner):
		# Get summoner champion ranked stats
		success, rankedStatsJSON = RANKED_STATS.getStats(summoner.summonerId)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner ranked stats JSON, got: %s" % rankedStatsJSON
		else:
			self.updateRankedStats(summoner, rankedStatsJSON)

	"""
	Adds entries with the summoners stats against the current game in the GameSummoners table.
	Updates the summoners ranked stats if appropriate, and spawns tasks to update the summoners
	champion stats.

	TODO: Consider moving this into a new "ProcessGameSummoner" task.
	"""
	def updateRankedStats(self, summoner, rankedStatsJSON):
		lastStatsModified = rankedStatsJSON["modifyDate"]

		# Initialize some stats we will collect
		totalSessionsWon = 0
		totalSessionsLost = 0
		totalGameChampionSessionsWon = 0
		totalGameChampionSessionsLost = 0

		# Update all the stats
		for championJSON in rankedStatsJSON["champions"]:
			# Champion id 0 is an aggregate of all stats - we use this for the summoner object
			if championJSON["id"] == 0:
				totalSessionsWon = championJSON["stats"]["totalSessionsWon"]
				totalSessionsLost = championJSON["stats"]["totalSessionsLost"]
			else:
				# Store the stats for the current champion id
				if championJSON["id"] == self.championId:
					totalGameChampionSessionsWon = championJSON["stats"]["totalSessionsWon"]
					totalGameChampionSessionsLost = championJSON["stats"]["totalSessionsLost"]
				self._updateSummonerChampionStats(lastStatsModified, summoner, championJSON)

		# Add the GameSummoners entry
		self.saveGameSummoner(summoner, totalSessionsWon, totalSessionsLost, totalGameChampionSessionsWon,
			totalGameChampionSessionsLost)

		# Update the summoner if necessary
		self._updateSummonerStats(lastStatsModified, summoner, totalSessionsWon, totalSessionsLost)

	"""
	Updates the summoner stats if necessary.

	TODO: Consider moving this into a new "ProcessGameSummoner" task.
	"""
	def _updateSummonerStats(self, lastStatsModified, summoner, totalSessionsWon, totalSessionsLost):
		# Check if we need to update the summoner stats
		if lastStatsModified > summoner.lastStatsModified:
			# Save the modified date
			summoner.lastStatsModified = lastStatsModified
			summoner.totalSessionsWon = totalSessionsWon
			summoner.totalSessionsLost = totalSessionsLost

	"""
	Updates the summoner champion stats if necessary.

	TODO: Consider moving this into a new "ProcessGameSummoner" task.
	"""
	def _updateSummonerChampionStats(self, lastStatsModified, summoner, championJSON):
		if lastStatsModified > summoner.lastStatsModified:
			summonerChampionTask = ProcessSummonerChampionTask(championJSON, summoner)
			summonerChampionTask.run()

	"""
	Saves the GameSummoner for this game and summoner with the relevant stats and champion image url.

	TODO: Consider moving this into a new "ProcessGameSummoner" task.
	"""
	def saveGameSummoner(self, summoner, totalSessionsWon, totalSessionsLost, totalGameChampionSessionsWon,
			totalGameChampionSessionsLost):
		# Get the current champion image URL
		# TODO: This should really be part of another system that maintains up to date links to static content,
		# but it'll do as a quick hack
		championImageUrl = getChampionImageUrl(CHAMPION_BY_ID.getChampionImageName(self.championId))

		# Create the GameSummoner domain object
		gameSummoner = GameSummoners(self.game.gameId, summoner.summonerId, totalSessionsWon, totalSessionsLost,
			totalGameChampionSessionsWon, totalGameChampionSessionsLost, self.teamId, self.championId, championImageUrl)

		DB.session.add(gameSummoner)

		# Add the summoner reference
		gameSummoner.summoner = summoner