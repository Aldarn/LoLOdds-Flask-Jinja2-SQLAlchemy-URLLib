#!/usr/bin/env/python2.7

import unittest
from src.hextech_project_x import APP
from src.services.game_odds_service import GAME_ODDS_SERVICE
from flask.ext.sqlalchemy import SQLAlchemy

class TestProcessSummonerChampionTask(unittest.TestCase):
	# Set the test config for the APP
	APP.config.from_object('test.test_config')

	# Create a DB handle from the app
	DB = SQLAlchemy(APP)

	def setUp(self):
		self.db = TestProcessSummonerChampionTask.DB
		# TODO: Create db & tables
		pass

	def tearDown(self):
		self.db.session.remove()
		self.db.drop_all()

	# def getGamesWithOdds(self):
	# 	games = Games.query.all()
	#
	# 	gameList = []
	# 	for game in games:
	# 		teams = defaultdict(list)
	# 		teamWinsAndLosses = defaultdict(lambda: defaultdict(int))
	# 		for summoner in game.summoners:
	# 			teamWinsAndLosses[summoner.teamId]["wins"] += summoner.totalSessionsWon
	# 			teamWinsAndLosses[summoner.teamId]["losses"] += summoner.totalSessionsLost
	# 			teams[summoner.teamId].append({
	# 				"name": summoner.name,
	# 				"championImageUrl": summoner.championImageUrl,
	# 				"winRate": self._getPercentage(summoner.totalSessionsWon, summoner.totalSessionsLost)
	# 			})
	#
	# 		# There's probably a better way of doing this, but at 3am i'm happy...
	# 		odds = self._calculateGameOdds(teamWinsAndLosses[teamWinsAndLosses.keys()[0]]["wins"],
	# 			teamWinsAndLosses[teamWinsAndLosses.keys()[0]]["losses"],
	# 			teamWinsAndLosses[teamWinsAndLosses.keys()[1]]["wins"],
	# 			teamWinsAndLosses[teamWinsAndLosses.keys()[1]]["losses"])
	#
	# 		gameList.append({ "teams": teams, "odds": odds, "mode": game.gameMode, "queue": game.gameQueueId })
	#
	# 	return gameList

	def testGetGamesWithOdds(self):
		# -------------------------------------------------------
		gamesWithOdds = GAME_ODDS_SERVICE.getGamesWithOdds()
		# -------------------------------------------------------
		self.assertTrue(isinstance(gamesWithOdds, dict))

	def testCalculateGameOdds(self):
		# -------------------------------------------------------
		odds = GAME_ODDS_SERVICE._calculateGameOdds(60, 40, 40, 60)
		# -------------------------------------------------------
		self.assertEqual(odds, "3 : 2")

	def testGetPercentage(self):
		# -------------------------------------------------------
		percentage = GAME_ODDS_SERVICE._getPercentage(10, 30)
		# -------------------------------------------------------
		self.assertEqual(percentage, 25)

	def testGetPercentageZero(self):
		# -------------------------------------------------------
		percentage = GAME_ODDS_SERVICE._getPercentage(0, 0)
		# -------------------------------------------------------
		self.assertEqual(percentage, 50)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
