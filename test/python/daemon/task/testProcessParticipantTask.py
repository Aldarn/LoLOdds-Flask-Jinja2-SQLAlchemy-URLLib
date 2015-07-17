#!/usr/bin/env/python2.7
# -*- coding: utf-8 -*-

import unittest
from src.api_daemon.tasks.process_participant_task import ProcessParticipantTask

class TestProcessParticipantTask(unittest.TestCase):
	def testRun(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("participant object not as expected")

	def testRunHandlesFailure(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("failure not handled")

	def testRunHandlesEmptyResults(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("empty results not handled")

	def testSave(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't save properly")

	def testUpdate(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't update properly")

	def testUpdateFromExisting(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't update from existing properly")

	def testSummonerUpdatedWithMoreRecentModifiedDate(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't update summoner with more recent modified date")

	def testSummonerNotUpdatedWithLessRecentModifiedDate(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("updated summoner with less recent modified date")

	def testRankedStatsUpdatedWithMoreRecentModifiedDate(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't update ranked stats with more recent modified date")

	def testRankedStatsNotUpdatedWithLessRecentModifiedDate(self):
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("updated ranked stats with less recent modified date")

	def testGetCurrentSummonerCrazyCharacters(self):
		crazyName = u"notíce me"
		# -------------------------------------------------------

		# -------------------------------------------------------
		self.fail("didn't get current summoner with crazy name")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
