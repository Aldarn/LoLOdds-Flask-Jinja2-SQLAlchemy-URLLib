#!/usr/bin/env/python2.7

import unittest
import src.api_daemon.daemon

class TestDaemon(unittest.TestCase):
	def testDaemonFetchesFeaturedGames(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("daemon does not fetch featured games")

	def testDaemonProcessesAllFeaturedGames(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("daemon does not process all featured games")

	def testDaemonRespectsClientRefreshInterval(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("daemon does not respect the client refresh interval")

	def testDaemonHandlesFailure(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("failure not handled")

	def testDaemonHandlesEmptyResults(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("empty results not handled")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
