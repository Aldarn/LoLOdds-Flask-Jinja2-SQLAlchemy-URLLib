#!/usr/bin/env/python2.7

import unittest
from src.api_daemon.tasks.process_featured_game_task import ProcessFeaturedGameTask
from mock import Mock, patch
from src.hextech_project_x import APP, DB
from src.domain.games import Games

class TestProcessFeaturedGameTask(unittest.TestCase):
	def setUp(self):
		APP.config.from_object('python.config')
		DB.session.close()
		DB.drop_all()
		DB.create_all()

		self.featuredGameJSON = {}
		self.task = ProcessFeaturedGameTask(self.featuredGameJSON)

	@patch.object(ProcessFeaturedGameTask, 'save')
	@patch('src.api_daemon.tasks.process_featured_game_task.ProcessParticipantTask')
	def testRun(self, processParticipantTaskMock, saveMock):
		self.task.featuredGameJSON = {"gameId": 1, "gameMode": "ARAM", "gameQueueConfigId": 4, "gameType": "MATCHED",
			"mapId": 1, "platformId": "EUW1", "participants": [{"summonerName": "soSleepy", "teamId": 100, "championId": 1},
			{"summonerName": "soClose", "teamId": 200, "championId": 56}]}

		processParticipantTaskMock.side_effect = lambda *args, **kwargs: Mock()
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		self.assertEquals(processParticipantTaskMock.call_count, 2)
		self.assertTrue(saveMock.called)

	def testSave(self):
		game = Games(1, "mode", 2, "type", 3, "EUW1")
		# -------------------------------------------------------
		self.task.save(game)
		# -------------------------------------------------------
		gameResults = Games.query.all()
		self.assertEquals(len(gameResults), 1)
		self.assertEquals(gameResults[0].gameId, 1)
		self.assertEquals(gameResults[0].gameMode, "mode")
		self.assertEquals(gameResults[0].gameQueueId, 2)
		self.assertEquals(gameResults[0].gameType, "type")
		self.assertEquals(gameResults[0].mapId, 3)
		self.assertEquals(gameResults[0].platformId, "EUW1")

	@patch.object(ProcessFeaturedGameTask, 'save')
	def testExistingGameNotSaved(self, saveMock):
		game = Games(1, "mode", 2, "type", 3, "EUW1")
		DB.session.add(game)
		DB.session.commit()

		self.task.featuredGameJSON = {"gameId": 1}
		# -------------------------------------------------------
		self.task.run()
		# -------------------------------------------------------
		self.assertFalse(saveMock.called)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
