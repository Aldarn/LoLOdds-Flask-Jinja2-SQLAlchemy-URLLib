#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
from src.api.summoner.summoner_by_name import SUMMONER_BY_NAME

class TestSummonerByNameAPIService(unittest.TestCase):
	@patch.object(SUMMONER_BY_NAME, '_getData')
	def testGetSummoners(self, getDataMock):
		# -------------------------------------------------------
		SUMMONER_BY_NAME.getSummoner("benholmes")
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = "benholmes")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
