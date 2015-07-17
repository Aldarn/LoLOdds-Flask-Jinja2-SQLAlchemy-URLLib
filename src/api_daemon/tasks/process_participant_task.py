# -*- coding: utf-8 -*-

from task import Task
from src.hextech_project_x import DB
from src.api.summoner.summoner_by_name import SUMMONER_BY_NAME
from src.api.stats.ranked_stats import RANKED_STATS
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
		# Get the existing summoner if we have already stored it
		summoner = self.getExistingSummoner()

		print "current summoner: %s" % summoner

		# Grab the summoner data from their name
		success, summonerJSON = SUMMONER_BY_NAME.getSummoner(self.participantName)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner by name, got: %s" % summonerJSON
		else:
			print "got summoner %s" % summonerJSON

			# Get the current champion image URL
			# TODO: This should really be part of another system that maintains up to date links to static content,
			# but it'll do as a quick hack
			championImageUrl = getChampionImageUrl(CHAMPION_BY_ID.getChampionImageName(self.championId))

			# For brevity - get the dictionary for the summoner name (there's only ever one key which corresponds
			# to the summoner name)
			summonerJSON = summonerJSON[summonerJSON.keys()[0]]

			# Update the existing summoner from the JSON
			if summoner:
				self.updateExistingSummoner(summoner, summonerJSON, championImageUrl)

			# Create a new summoner from the JSON
			else:
				summoner = self.save(summonerJSON, championImageUrl)

			# Process the ranked stats
			self.processRankedStats(summoner)

	"""
	Gets the ranked stats for this summoner and updates them if they have changed, otherwise it updates
	the summoner if that has changed.

	My justification for this method being in this task instead of the SummonerChampionTask is that
	this is dealing with updating the summoner and creating new champion entries only if the ranked stats
	have changed, and also setting aggregate stats directly on the summoner object.
	"""
	def processRankedStats(self, summoner):
		# Get summoner champion ranked stats
		success, rankedStatsJSON = RANKED_STATS.getStats(summoner.summonerId)

		if not success:
			# TODO: Log this properly
			# TODO: What should we do about it?
			print "Failed to get summoner ranked stats JSON, got: %s" % rankedStatsJSON
		else:
			# Check if we need to update the stats
			lastStatsModified = rankedStatsJSON["modifyDate"]
			if lastStatsModified > summoner.lastStatsModified:
				# Save the modified date
				summoner.lastStatsModified = lastStatsModified

				self.updateRankedStats(summoner, rankedStatsJSON)

	"""
	Updates the summoners ranked stats if appropriate, and spawns tasks to update the summoners
	champion stats.
	"""
	def updateRankedStats(self, summoner, rankedStatsJSON):
		# Update all the stats
		for championJSON in rankedStatsJSON["champions"]:
			# Champion id 0 is an aggregate of all stats - we use this for the summoner object
			if championJSON["id"] == 0:
				summoner.totalSessionsWon = championJSON["stats"]["totalSessionsWon"]
				summoner.totalSessionsLost = championJSON["stats"]["totalSessionsLost"]
			else:
				summonerChampionTask = ProcessSummonerChampionTask(championJSON, summoner)
				summonerChampionTask.run()

	"""
	Gets an existing summoner object from the database.
	"""
	def getExistingSummoner(self):
		# Get the existing summoner if it exists
		try:
			return Summoners.query.filter_by(name = self.participantName).first()
		except OperationalError, oe:
			print "Error loading current summoner: %s" % oe
		return None

	"""
	Creates a brand new summoner domain object.
	"""
	def save(self, summonerJSON, championImageUrl):
		# Last stats modified and total wins / losses will be set by the champion with id 0 once we grab them shortly
		summoner = Summoners(int(summonerJSON["id"]), summonerJSON["name"], getProfileIconUrl(summonerJSON["profileIconId"]),
			int(summonerJSON["revisionDate"]), 0, int(summonerJSON["summonerLevel"]), 0, 0, int(self.teamId),
			int(self.championId), championImageUrl)

		# Add it to the game so we get a relation
		self.game.summoners.append(summoner)

		return summoner

	"""
	Updates an existing summoner object if necessary.
	"""
	def updateExistingSummoner(self, summoner, summonerJSON, championImageUrl):
		# Add it to the game so we get a relation
		self.game.summoners.append(summoner)

		newLastModified = int(summonerJSON["revisionDate"])
		if newLastModified > summoner.lastModified:
			summoner.name = summonerJSON["name"]
			summoner.iconImageUrl = getProfileIconUrl(summonerJSON["profileIconId"])
			summoner.lastModified = newLastModified
			summoner.level = int(summonerJSON["summonerLevel"])
			summoner.teamId = int(self.teamId)
			summoner.championId = int(self.championId)
			summoner.championImageUrl = championImageUrl
