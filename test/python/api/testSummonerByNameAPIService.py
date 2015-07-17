#!/usr/bin/env/python2.7
# -*- coding: utf-8 -*-

import unittest
from mock import patch, Mock, MagicMock
from src.api.summoner.summoner_by_name import SUMMONER_BY_NAME

class TestSummonerByNameAPIService(unittest.TestCase):
	@patch.object(SUMMONER_BY_NAME, '_getData')
	def testGetSummoner(self, getDataMock):
		# -------------------------------------------------------
		SUMMONER_BY_NAME.getSummoner("benholmes")
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = "benholmes")

	def testGetAPIFriendlySummonerName(self):
		crazyName = u"notíce me"
		# -------------------------------------------------------
		result = SUMMONER_BY_NAME._getAPIFriendlySummonerName(crazyName)
		# -------------------------------------------------------
		self.assertEquals(result, "not%c3%adceme")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
