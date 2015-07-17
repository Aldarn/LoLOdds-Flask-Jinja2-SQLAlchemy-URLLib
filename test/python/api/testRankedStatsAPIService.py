#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
from src.api.stats.ranked_stats import RANKED_STATS

class TestRankedStatsAPIService(unittest.TestCase):
	@patch.object(RANKED_STATS, '_getData')
	def testGetStats(self, getDataMock):
		# -------------------------------------------------------
		RANKED_STATS.getStats(123)
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = "123/ranked")

	@patch.object(RANKED_STATS, '_getData')
	def testGetStatsWithSeason(self, getDataMock):
		# -------------------------------------------------------
		RANKED_STATS.getStats(123, RANKED_STATS.VALID_SEASONS[0])
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = "123/ranked", season = RANKED_STATS.VALID_SEASONS[0])

	@patch.object(RANKED_STATS, '_getData')
	def testGetStatsWithInvalidSeason(self, getDataMock):
		# -------------------------------------------------------
		RANKED_STATS.getStats(123, "bla")
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = "123/ranked")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
