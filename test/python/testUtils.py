#!/usr/bin/env/python2.7

import unittest
import src.utils as utils

class TestUtils(unittest.TestCase):
	def testGetProfileIconUrl(self):
		# -------------------------------------------------------
		url = utils.getProfileIconUrl(123)
		# -------------------------------------------------------
		self.assertEquals(url, "http://ddragon.leagueoflegends.com/cdn/5.13.1/img/profileicon/123.png")

	def testGetChmapionImageUrl(self):
		# -------------------------------------------------------
		url = utils.getChampionImageUrl("JarvanIV.png")
		# -------------------------------------------------------
		self.assertEquals(url, "http://ddragon.leagueoflegends.com/cdn/5.2.1/img/champion/JarvanIV.png")

def main():
	unittest.main()

if __name__ == '__main__':
	main()
