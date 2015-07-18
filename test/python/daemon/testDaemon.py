#!/usr/bin/env/python2.7

import unittest
import src.api_daemon.daemon as daemon
from mock import Mock, patch

class TestDaemon(unittest.TestCase):
	@patch('src.api_daemon.daemon.FEATURED_GAMES')
	@patch('src.api_daemon.daemon.time')
	def testDaemonFetchesFeaturedGames(self, timeMock, featuredGamesMock):
		breakLoopException = Exception("break")
		timeMock.sleep.side_effect = breakLoopException
		featuredGamesMock.getFeaturedGames.return_value = (False, None)
		# -------------------------------------------------------
		try:
			daemon.run()
		except Exception, e:
			self.assertEquals(e, breakLoopException)
		# -------------------------------------------------------
		self.assertTrue(featuredGamesMock.getFeaturedGames.called)

	@patch('src.api_daemon.daemon.FEATURED_GAMES')
	@patch('src.api_daemon.daemon.time')
	@patch('src.api_daemon.daemon.ProcessFeaturedGameTask')
	def testDaemonRespectsClientRefreshInterval(self, processFeaturedGameTaskMock, timeMock, featuredGamesMock):
		featuredGamesJSON = {"clientRefreshInterval": 100, "gameList": [{}, {}]}

		breakLoopException = Exception("break")
		timeMock.sleep.side_effect = breakLoopException
		featuredGamesMock.getFeaturedGames.return_value = (True, featuredGamesJSON)
		# -------------------------------------------------------
		try:
			daemon.run()
		except Exception, e:
			self.assertEquals(e, breakLoopException)
		# -------------------------------------------------------
		timeMock.sleep.assert_called_with(100)

	@patch('src.api_daemon.daemon.FEATURED_GAMES')
	@patch('src.api_daemon.daemon.time')
	@patch('src.api_daemon.daemon.ProcessFeaturedGameTask')
	def testDaemonProcessesAllFeaturedGames(self, processFeaturedGameTaskMock, timeMock, featuredGamesMock):
		featuredGamesJSON = {"clientRefreshInterval": 100, "gameList": [{}, {}]}

		breakLoopException = Exception("break")
		timeMock.sleep.side_effect = breakLoopException
		featuredGamesMock.getFeaturedGames.return_value = (True, featuredGamesJSON)

		processFeaturedGameTaskMock.side_effect = lambda *args, **kwargs: Mock()
		# -------------------------------------------------------
		try:
			daemon.run()
		except Exception, e:
			self.assertEquals(e, breakLoopException)
		# -------------------------------------------------------
		self.assertEquals(processFeaturedGameTaskMock.call_count, 2)

	@patch('src.api_daemon.daemon.FEATURED_GAMES')
	@patch('src.api_daemon.daemon.time')
	def testDaemonHandlesFailure(self, timeMock, featuredGamesMock):
		breakLoopException = Exception("break")
		timeMock.sleep.side_effect = breakLoopException
		featuredGamesMock.getFeaturedGames.return_value = (False, None)
		# -------------------------------------------------------
		try:
			daemon.run()
		except Exception, e:
			self.assertEquals(e, breakLoopException)
		# -------------------------------------------------------
		timeMock.sleep.assert_called_with(1)

	@patch('src.api_daemon.daemon.FEATURED_GAMES')
	@patch('src.api_daemon.daemon.time')
	def testDaemonHandlesEmptyResults(self, timeMock, featuredGamesMock):
		featuredGamesJSON = {"clientRefreshInterval": 100, "gameList": []}

		breakLoopException = Exception("break")
		timeMock.sleep.side_effect = breakLoopException
		featuredGamesMock.getFeaturedGames.return_value = (True, featuredGamesJSON)
		# -------------------------------------------------------
		try:
			daemon.run()
		except Exception, e:
			self.assertEquals(e, breakLoopException)
		# -------------------------------------------------------
		timeMock.sleep.assert_called_with(1)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
