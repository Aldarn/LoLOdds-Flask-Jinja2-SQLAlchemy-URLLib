#!/usr/bin/env/python2.7

import unittest
import src.utils as utils

class TestUtils(unittest.TestCase):
	def testGetProfileIconUrl(self):
		# -------------------------------------------------------
		url = utils.getProfileIconUrl(123)
		# -------------------------------------------------------
		self.assertEquals(url, "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/profileicon/123.png")

	def testGetChmapionImageUrl(self):
		# -------------------------------------------------------
		url = utils.getChampionImageUrl("JarvanIV.png")
		# -------------------------------------------------------
		self.assertEquals(url, "http://ddragon.leagueoflegends.com/cdn/5.14.1/img/champion/JarvanIV.png")

	def testGetTeamNamePurple(self):
		# -------------------------------------------------------
		teamName = utils.getTeamName(100)
		# -------------------------------------------------------
		self.assertEquals(teamName, "PURPLE")

	def testGetTeamNameBlue(self):
		# -------------------------------------------------------
		teamName = utils.getTeamName(200)
		# -------------------------------------------------------
		self.assertEquals(teamName, "BLUE")

	def testGetTeamNameUnknown(self):
		# -------------------------------------------------------
		teamName = utils.getTeamName(9001)
		# -------------------------------------------------------
		self.assertEquals(teamName, "UNKNOWN")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
