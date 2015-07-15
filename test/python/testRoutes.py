#!/usr/bin/env/python2.7

import unittest
import mock
import src.hextech_project_x as hpx

class TestRoutes(unittest.TestCase):
	@mock.patch('src.hextech_project_x.render_template')
	def testIndex(self, render_template):
		# -------------------------------------------------------
		result = hpx.index()
		# -------------------------------------------------------
		render_template.assert_called_with('index.html')

def main():
	unittest.main()

if __name__ == '__main__':
	main()
