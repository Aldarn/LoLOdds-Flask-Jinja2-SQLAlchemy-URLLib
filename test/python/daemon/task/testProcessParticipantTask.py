#!/usr/bin/env/python2.7
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, patch
from src.api_daemon.tasks.process_participant_task import ProcessParticipantTask
from src.hextech_project_x import APP, DB
from src.domain.games import Games
from src.domain.summoners import Summoners
from src.domain.game_summoners import GameSummoners
from src.utils import getProfileIconUrl

class TestProcessParticipantTask(unittest.TestCase):
	def setUp(self):
		APP.config.from_object('python.config')
		DB.session.close()
		DB.drop_all()
		DB.create_all()

		game = Games(1, "mode", 2, "type", 3, "EUW1")
		DB.session.add(game)
		DB.session.commit()

		self.task = ProcessParticipantTask(u"name", 1, 1, game)

	@patch('src.api_daemon.tasks.process_participant_task.SUMMONER_BY_NAME')
	@patch.object(ProcessParticipantTask, 'getExistingSummoner')
	@patch.object(ProcessParticipantTask, '_updateExistingSummoner')
	@patch.object(ProcessParticipantTask, 'processRankedStats')
	# TODO: Test this more granularly
	def testRunExistingSummoner(self, processRankedStatsMock, updateExistingSummonerMock, getExistingSummonerMock, summonerByNameMock):
		summonerJSON = {u"name": { "bla": "yes" }}

		getExistingSummonerMock.return_value = "summoner"
		summonerByNameMock.getSummoner.return_value = (True, summonerJSON)
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		updateExistingSummonerMock.assert_called_with("summoner", { "bla": "yes"  })
		processRankedStatsMock.assert_called_with("summoner")

	@patch('src.api_daemon.tasks.process_participant_task.SUMMONER_BY_NAME')
	@patch.object(ProcessParticipantTask, 'getExistingSummoner')
	@patch.object(ProcessParticipantTask, 'save')
	@patch.object(ProcessParticipantTask, 'processRankedStats')
	# TODO: Test this more granularly
	def testRunNewSummoner(self, processRankedStatsMock, saveMock, getExistingSummonerMock, summonerByNameMock):
		summonerJSON = {u"name": { "bla": "yes" }}

		getExistingSummonerMock.return_value = None
		summonerByNameMock.getSummoner.return_value = (True, summonerJSON)
		saveMock.return_value = "summoner"
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		saveMock.assert_called_with({ "bla": "yes" })
		processRankedStatsMock.assert_called_with("summoner")

	@patch.object(ProcessParticipantTask, 'saveGameSummoner')
	@patch.object(ProcessParticipantTask, '_updateSummonerStats')
	@patch.object(ProcessParticipantTask, '_updateSummonerChampionStats')
	# TODO: Test this more granularly
	def testUpdateRankedStats(self, updateSummonerChampionStatsMock, updateSummonerStatsMock, saveGameSummonerMock):
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()

		rankedStatsJSON = {"modifyDate": 999, "champions": [{ "id": 0, "stats": {"totalSessionsWon": 5, "totalSessionsLost": 10}},
			{ "id": 1, "stats": {"totalSessionsWon": 2, "totalSessionsLost": 3}}]}
		# -------------------------------------------------------
		self.task.updateRankedStats(summoner, rankedStatsJSON)
		# -------------------------------------------------------
		updateSummonerChampionStatsMock.assert_called_with(999, summoner, { "id": 1, "stats": {"totalSessionsWon": 2, "totalSessionsLost": 3}})
		saveGameSummonerMock.assert_called_with(summoner, 5, 10, 2, 3)
		updateSummonerStatsMock.assert_called_with(999, summoner, 5, 10)

	def testGetExistingSummonerNoSummoner(self):
		# -------------------------------------------------------
		summoner = self.task.getExistingSummoner()
		# -------------------------------------------------------
		self.assertEquals(summoner, None)

	def testGetExistingSummonerCrazyCharacters(self):
		crazyName = u"notíce me"
		crazySummoner = Summoners(1, crazyName, "iconImageUrl", 1, 1, 30, 1, 1)
		DB.session.add(crazySummoner)
		DB.session.commit()

		self.task.participantName = crazyName
		# -------------------------------------------------------
		summoner = self.task.getExistingSummoner()
		# -------------------------------------------------------
		self.assertEquals(summoner.summonerId, 1)
		self.assertEquals(summoner.name, crazyName)

	def testSave(self):
		summonerJSON = {"id": 10, "name": u"whatevs", "profileIconId": "5", "revisionDate": 1, "summonerLevel": 20}
		# -------------------------------------------------------
		summoner = self.task.save(summonerJSON)
		# -------------------------------------------------------
		self.assertEquals(summoner.summonerId, 10)
		self.assertEquals(summoner.name, u"whatevs")
		self.assertEquals(summoner.iconImageUrl, getProfileIconUrl(5))
		self.assertEquals(summoner.lastModified, 1)
		self.assertEquals(summoner.level, 20)

	def testUpdateExistingSummonerModified(self):
		summonerJSON = {"revisionDate": 100, "name": u"bla", "profileIconId": 321, "summonerLevel": 25}
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()
		# -------------------------------------------------------
		self.task._updateExistingSummoner(summoner, summonerJSON)
		# -------------------------------------------------------
		self.assertEquals(summoner.name, u"bla")
		self.assertEquals(summoner.iconImageUrl, getProfileIconUrl(321))
		self.assertEquals(summoner.lastModified, 100)
		self.assertEquals(summoner.level, 25)

	def testUpdateExistingSummonerNotModified(self):
		summonerJSON = {"revisionDate": 0, "name": u"bla", "profileIconId": 321, "summonerLevel": 25}
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()
		# -------------------------------------------------------
		self.task._updateExistingSummoner(summoner, summonerJSON)
		# -------------------------------------------------------
		self.assertNotEquals(summoner.name, u"bla")

	def testUpdateSummonerStatsModified(self):
		lastStatsModified = 100
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()
		totalSessionsWon = 10
		totalSessionsLost = 100
		# -------------------------------------------------------
		self.task._updateSummonerStats(lastStatsModified, summoner, totalSessionsWon, totalSessionsLost)
		# -------------------------------------------------------
		self.assertEquals(summoner.lastStatsModified, lastStatsModified)
		self.assertEquals(summoner.totalSessionsWon, totalSessionsWon)
		self.assertEquals(summoner.totalSessionsLost, totalSessionsLost)

	def testUpdateSummonerStatsNotModified(self):
		lastStatsModified = 0
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()
		totalSessionsWon = 10
		totalSessionsLost = 100
		# -------------------------------------------------------
		self.task._updateSummonerStats(lastStatsModified, summoner, totalSessionsWon, totalSessionsLost)
		# -------------------------------------------------------
		self.assertNotEquals(summoner.lastStatsModified, lastStatsModified)

	@patch('src.api_daemon.tasks.process_participant_task.ProcessSummonerChampionTask')
	# TODO: This is a bit dodgy...
	def testUpdateSummonerChampionStats(self, processSummonerChampionTaskMock):
		lastStatsModified = 100
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()

		errorException = Exception("error")
		processSummonerChampionTaskMock.side_effect = errorException
		# -------------------------------------------------------
		try:
			self.task._updateSummonerChampionStats(lastStatsModified, summoner, {})
			self.fail("ProcessSummonerChampionTask was not instantiated")
		except:
			pass
		# -------------------------------------------------------

	@patch('src.api_daemon.tasks.process_participant_task.ProcessSummonerChampionTask')
	# TODO: This is a bit dodgy...
	def testUpdateSummonerChampionStatsNotModified(self, processSummonerChampionTaskMock):
		lastStatsModified = 0
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()

		errorException = Exception("error")
		processSummonerChampionTaskMock.side_effect = errorException
		# -------------------------------------------------------
		try:
			self.task._updateSummonerChampionStats(lastStatsModified, summoner, {})
		except:
			self.fail("ProcessSummonerChampionTask was instantiated")
		# -------------------------------------------------------

	@patch('src.api_daemon.tasks.process_participant_task.getChampionImageUrl')
	def testSaveGameSummoner(self, getChampionImageUrlMock):
		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()

		totalSessionsWon = 10
		totalSessionsLost = 100
		totalGameChampionSessionsWon = 5
		totalGameChampionSessionsLost = 50

		getChampionImageUrlMock.return_value = "championImageUrl"
		# -------------------------------------------------------
		self.task.saveGameSummoner(summoner, totalSessionsWon, totalSessionsLost, totalGameChampionSessionsWon,
			totalGameChampionSessionsLost)
		# -------------------------------------------------------
		gameSummoners = GameSummoners.query.all()
		self.assertEquals(len(gameSummoners), 1)
		self.assertEquals(gameSummoners[0].gameId, 1)
		self.assertEquals(gameSummoners[0].summonerId, 1)
		self.assertEquals(gameSummoners[0].totalSessionsWon, totalSessionsWon)
		self.assertEquals(gameSummoners[0].totalSessionsLost, totalSessionsLost)
		self.assertEquals(gameSummoners[0].totalChampionSessionsWon, totalGameChampionSessionsWon)
		self.assertEquals(gameSummoners[0].totalChampionSessionsLost, totalGameChampionSessionsLost)
		self.assertEquals(gameSummoners[0].teamId, 1)
		self.assertEquals(gameSummoners[0].championId, 1)
		self.assertEquals(gameSummoners[0].championImageUrl, "championImageUrl")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
