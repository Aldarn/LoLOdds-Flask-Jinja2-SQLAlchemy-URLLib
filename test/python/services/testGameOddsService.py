#!/usr/bin/env/python2.7

import unittest
from src.hextech_project_x import APP, DB
from src.services.game_odds_service import GAME_ODDS_SERVICE
from src.domain.games import Games
from src.domain.summoners import Summoners
from src.domain.game_summoners import GameSummoners

class TestGameOddsService(unittest.TestCase):
	def setUp(self):
		APP.config.from_object('src.resources.test_config')
		DB.session.close()
		DB.drop_all()
		DB.create_all()

	# TODO: Should test this method at a more granular level, since this is basically an integration test
	def testGetGamesWithOdds(self):
		blueSummoner = Summoners(1, u"name", "iconImageUrl", 1, 1, 30, 10, 90)
		blueGameSummoner = GameSummoners(1, 1, 5, 15, 10, 90, 200, 1, "championImageUrl")
		blueGameSummoner.summoner = blueSummoner

		purpleSummoner = Summoners(2, u"name", "iconImageUrl", 1, 1, 30, 1, 1)
		purpleGameSummoner = GameSummoners(1, 2, 3, 7, 9, 1, 100, 1, "championImageUrl")
		purpleGameSummoner.summoner = purpleSummoner

		game = Games(1, "mode", 2, "type", 3, "EUW1")
		game.summoners.append(blueGameSummoner)
		game.summoners.append(purpleGameSummoner)
		DB.session.add(game)
		DB.session.commit()
		# -------------------------------------------------------
		gamesWithOdds = GAME_ODDS_SERVICE.getGamesWithOdds()
		# -------------------------------------------------------
		self.assertEqual(len(gamesWithOdds), 1)
		self.assertEqual(gamesWithOdds[0]["odds"], "9 : 11")
		self.assertEqual(gamesWithOdds[0]["championOdds"], "1 : 9")
		self.assertEqual(gamesWithOdds[0]["teams"]["BLUE"][0]["winRate"], 25)
		self.assertEqual(gamesWithOdds[0]["teams"]["BLUE"][0]["championWinRate"], 10)
		self.assertEqual(gamesWithOdds[0]["teams"]["PURPLE"][0]["winRate"], 30)
		self.assertEqual(gamesWithOdds[0]["teams"]["PURPLE"][0]["championWinRate"], 90)

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
