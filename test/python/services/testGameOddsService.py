#!/usr/bin/env/python2.7

import unittest
from src.services.game_odds_service import GAME_ODDS_SERVICE

class TestProcessSummonerChampionTask(unittest.TestCase):
	def testGetGamesWithOdds(self):
		# -------------------------------------------------------
		gamesWithOdds = GAME_ODDS_SERVICE.getGamesWithOdds()
		# -------------------------------------------------------
		self.assertTrue(isinstance(gamesWithOdds, dict))

def main():
	unittest.main()

if __name__ == '__main__':
	main()
