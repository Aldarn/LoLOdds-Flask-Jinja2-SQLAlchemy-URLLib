#!/usr/bin/env/python2.7

import unittest
import mock
import src.hextech_project_x as hpx

class TestRoutes(unittest.TestCase):
	@mock.patch('src.hextech_project_x.render_template')
	@mock.patch('src.hextech_project_x.GAME_ODDS_SERVICE.getGamesWithOdds')
	def testIndex(self, getGameOddsMock, render_template):
		getGameOddsMock.return_value = [{}]
		# -------------------------------------------------------
		result = hpx.index()
		# -------------------------------------------------------
		render_template.assert_called_with('index.html', currentGameOdds = [{}])

	@mock.patch('src.hextech_project_x.render_template')
	@mock.patch('src.hextech_project_x.GAME_ODDS_SERVICE.getGamesWithOdds')
	def testIndexShowsNoGames(self, getGameOddsMock, render_template):
		getGameOddsMock.return_value = []
		# -------------------------------------------------------
		result = hpx.index()
		# -------------------------------------------------------
		render_template.assert_called_with('nogames.html')

def main():
	unittest.main()

if __name__ == '__main__':
	main()
