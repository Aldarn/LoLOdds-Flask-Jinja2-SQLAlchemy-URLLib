#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
from src.api.featured_games.featured_games import FEATURED_GAMES

class TestFeaturedGamesAPIService(unittest.TestCase):
	@patch.object(FEATURED_GAMES, '_getData')
	def testGetFeaturedGames(self, getDataMock):
		getDataMock.return_value = {"gameId": 1}
		# -------------------------------------------------------
		result = FEATURED_GAMES.getFeaturedGames()
		# -------------------------------------------------------
		self.assertEquals(result, {"gameId": 1})

def main():
	unittest.main()

if __name__ == '__main__':
	main()
