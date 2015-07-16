#!/usr/bin/env/python2.7

import unittest
import mock
import src.resources.config as config
from src.api.api_service import APIService

class TestRoutes(unittest.TestCase):
	class TestAPIService(APIService):
		def __init__(self):
			super(TestRoutes.TestAPIService, self).__init__("bla.com/bla")
		def _onFail(self, result):
			self.failResult = result
		def _onSuccess(self, result):
			self.successResult = result

	def setUp(self):
		self.apiService = TestRoutes.TestAPIService()
		config.API_KEY = "testKey"

	def testGetEndpointCorrectFormat(self):
		# -------------------------------------------------------
		result = self.apiService.getEndpoint()
		# -------------------------------------------------------
		self.assertEquals(result, "bla.com/bla?api_key=testKey")

	@mock.patch('src.api.api_service.urllib2')
	def testGetDataParams(self, urllibMock):
		# -------------------------------------------------------
		self.apiService.getData(thing = "sup")
		# -------------------------------------------------------
		urllibMock.urlopen.assert_called_with("todo")

	@mock.patch('src.api.api_service.urllib2.urlopen', mock.MagicMock(return_value = '{"test": "yup"}'))
	def testGetDataSuccessCallsOnSuccess(self):
		# -------------------------------------------------------
		self.apiService.getData()
		# -------------------------------------------------------
		self.assertEquals(self.apiService.successResult, {"test": "yup"})

	@mock.patch('src.api.api_service.urllib2.urlopen', mock.MagicMock(return_value = '{"status": {"status_code": 404}}'))
	def testGetDataFailCallsOnFail(self):
		# -------------------------------------------------------
		self.apiService.getData()
		# -------------------------------------------------------
		self.assertEquals(self.apiService.failResult, {"status": {"status_code": 404}})

	@mock.patch('src.api.api_service.urllib2')
	def testGetDataErrorCallsOnFail(self, urllibMock):
		errorException = Exception("Error")
		urllibMock.side_effect = errorException
		# -------------------------------------------------------
		self.assertRaises(errorException, self.apiService.getData)
		# -------------------------------------------------------

def main():
	unittest.main()

if __name__ == '__main__':
	main()
