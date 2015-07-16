#!/usr/bin/env/python2.7

import unittest
from src.api.featured_games.featured_games import FEATURED_GAMES

class TestFeaturedGamesAPIService(unittest.TestCase):
	def testOnSuccess(self):
		# -------------------------------------------------------
		FEATURED_GAMES._onSuccess(None)
		# -------------------------------------------------------
		self.fail("what to do")

	def testOnFail(self):
		# -------------------------------------------------------
		FEATURED_GAMES._onFail(None)
		# -------------------------------------------------------
		self.fail("what to do")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
