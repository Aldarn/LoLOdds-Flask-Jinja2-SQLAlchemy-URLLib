#!/usr/bin/env/python2.7

import unittest
from mock import Mock, patch
from src.hextech_project_x import APP, DB
from src.domain.summoners import Summoners
from src.api_daemon.tasks.process_summoner_champion_task import ProcessSummonerChampionTask
from src.domain.summoner_champion_stats import SummonerChampionStats

class TestProcessSummonerChampionTask(unittest.TestCase):
	def setUp(self):
		APP.config.from_object('python.config')
		DB.session.close()
		DB.drop_all()
		DB.create_all()

		summoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		DB.session.add(summoner)
		DB.session.commit()

		championJSON = {}
		self.task = ProcessSummonerChampionTask(championJSON, summoner)

	@patch.object(ProcessSummonerChampionTask, 'save')
	def testRunSavesNewChampionStats(self, saveMock):
		self.task.championJSON = {"id": 10}
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		saveMock.assert_called_with(10)

	@patch.object(ProcessSummonerChampionTask, 'updateExistingChampionStats')
	def testRunUpdatesExistingChampionStats(self, updateExistingChampionStatsMock):
		self.task.championJSON = {"id": 10}
		summonerChampionStats = SummonerChampionStats(1, 10, 100, 1000)
		DB.session.add(summonerChampionStats)
		DB.session.commit()
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		updateExistingChampionStatsMock.assert_called_with(summonerChampionStats)

	def testSave(self):
		self.task.championJSON = {"id": 10, "stats": {"totalSessionsWon": 100, "totalSessionsLost": 1000}}
		# -------------------------------------------------------
		self.task.save(10)
		# -------------------------------------------------------
		championStatsResults = SummonerChampionStats.query.all()
		self.assertEquals(len(championStatsResults), 1)
		self.assertEquals(championStatsResults[0].summonerId, 1)
		self.assertEquals(championStatsResults[0].championId, 10)
		self.assertEquals(championStatsResults[0].totalSessionsWon, 100)
		self.assertEquals(championStatsResults[0].totalSessionsLost, 1000)

	def testUpdateExistingChampionStats(self):
		self.task.championJSON = {"id": 10, "stats": {"totalSessionsWon": 56, "totalSessionsLost": 22}}
		championStats = Mock()
		# -------------------------------------------------------
		self.task.updateExistingChampionStats(championStats)
		# -------------------------------------------------------
		self.assertEquals(championStats.totalSessionsWon, 56)
		self.assertEquals(championStats.totalSessionsLost, 22)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
