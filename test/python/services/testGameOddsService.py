#!/usr/bin/env/python2.7

import unittest
from src.services.game_odds_service import GAME_ODDS_SERVICE

class TestProcessSummonerChampionTask(unittest.TestCase):
	# TODO: Setup test DB

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
