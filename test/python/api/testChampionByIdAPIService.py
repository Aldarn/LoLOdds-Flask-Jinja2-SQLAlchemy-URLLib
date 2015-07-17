#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
from src.api.static.champion_by_id import CHAMPION_BY_ID

class TestRankedStatsAPIService(unittest.TestCase):
	@patch.object(CHAMPION_BY_ID, '_getData')
	def testGetChampion(self, getDataMock):
		# -------------------------------------------------------
		CHAMPION_BY_ID.getChampion(59)
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = 59)

	@patch.object(CHAMPION_BY_ID, '_getData')
	def testGetChampionImageNameCorrectCall(self, getDataMock):
		getDataMock.return_value = False, "fake"
		# -------------------------------------------------------
		CHAMPION_BY_ID.getChampionImageName(56)
		# -------------------------------------------------------
		getDataMock.assert_called_with(endpoint = 56, champData = "image")

	@patch.object(CHAMPION_BY_ID, '_getData')
	def testGetChampionImageName(self, getDataMock):
		getDataMock.return_value = True, { "image": { "full": "Caitlyn.png" } }
		# -------------------------------------------------------
		data = CHAMPION_BY_ID.getChampionImageName(51)
		# -------------------------------------------------------
		self.assertEquals(data, "Caitlyn.png")

	@patch.object(CHAMPION_BY_ID, '_getData')
	def testGetChampionImageNameHandlesFailure(self, getDataMock):
		getDataMock.return_value = False, "bla"
		# -------------------------------------------------------
		success, data = CHAMPION_BY_ID.getChampionImageName(51)
		# -------------------------------------------------------
		self.assertEquals(success, False)
		self.assertEquals(data, "bla")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
