#!/usr/bin/env/python2.7
# -*- coding: utf-8 -*-

import unittest
from mock import Mock, patch
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

	# def updateRankedStats(self, summoner, lastStatsModified, rankedStatsJSON):
	# 	# Save the modified date
	# 	summoner.lastStatsModified = lastStatsModified
	#
	# 	# Update all the stats
	# 	for championJSON in rankedStatsJSON["champions"]:
	# 		# Champion id 0 is an aggregate of all stats - we use this for the summoner object
	# 		if championJSON["id"] == 0:
	# 			summoner.totalSessionsWon = championJSON["stats"]["totalSessionsWon"]
	# 			summoner.totalSessionsLost = championJSON["stats"]["totalSessionsLost"]
	# 		else:
	# 			summonerChampionTask = ProcessSummonerChampionTask(championJSON, summoner)
	# 			summonerChampionTask.run()
	#
	# 	# Commit the changes
	# 	self.update(summoner)

	@patch.object(ProcessParticipantTask, 'update')
	def testUpdateRankedStatsCallsUpdate(self, updateMock):
		game = Mock()
		summoner = Mock()
		lastStatsModified = 1
		rankedStatsJSON = { "champions": [] }
		task = ProcessParticipantTask("name", 1, 2, game)
		# -------------------------------------------------------
		task.updateRankedStats(summoner, lastStatsModified, rankedStatsJSON)
		# -------------------------------------------------------
		updateMock.assert_called_with(summoner)

	@patch.object(ProcessParticipantTask, 'update')
	def testUpdateRankedStatsSetsSummonerStats(self, updateMock):
		game = Mock()
		summoner = Mock()
		lastStatsModified = 1
		rankedStatsJSON = { "champions": [{"id": 0, "stats": { "totalSessionsWon": 5, "totalSessionsLost": 50 } }] }
		task = ProcessParticipantTask("name", 1, 2, game)
		# -------------------------------------------------------
		task.updateRankedStats(summoner, lastStatsModified, rankedStatsJSON)
		# -------------------------------------------------------
		self.assertEquals(summoner.totalSessionsWon, 5)
		self.assertEquals(summoner.totalSessionsLost, 50)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
