#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
import src.resources.config as config
from src.api.api_service import APIService

class TestAPIService(unittest.TestCase):
	class TestAPIService(APIService):
		def __init__(self):
			super(TestAPIService.TestAPIService, self).__init__("bla.com/bla")
		def _onFail(self, result):
			self.failResult = result
		def _onSuccess(self, result):
			self.successResult = result

	def setUp(self):
		self.apiService = TestAPIService.TestAPIService()
		config.API_KEY = "testKey"

	def testGetEndpointCorrectFormat(self):
		# -------------------------------------------------------
		result = self.apiService.getEndpoint()
		# -------------------------------------------------------
		self.assertEquals(result, "bla.com/bla?api_key=testKey")

	@patch('src.api.api_service.urllib2')
	def testGetDataParams(self, urllibMock):
		# -------------------------------------------------------
		self.apiService.getData(thing = "sup")
		# -------------------------------------------------------
		urllibMock.urlopen.assert_called_with("bla.com/bla?api_key=testKey&thing=sup")

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataSuccessCallsOnSuccess(self, urlOpenMock):
		urlOpenResponse = Mock()
		urlOpenResponse.read.side_effect = ['{"test": "yup"}']
		urlOpenMock.return_value = urlOpenResponse
		# -------------------------------------------------------
		self.apiService.getData()
		# -------------------------------------------------------
		self.assertEquals(self.apiService.successResult, {"test": "yup"})

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataFailCallsOnFail(self, urlOpenMock):
		urlOpenResponse = Mock()
		urlOpenResponse.read.side_effect = ['{"status": {"status_code": 404}}']
		urlOpenMock.return_value = urlOpenResponse
		# -------------------------------------------------------
		self.apiService.getData()
		# -------------------------------------------------------
		self.assertEquals(self.apiService.failResult, {"status": {"status_code": 404}})

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataErrorCallsOnFail(self, urlOpenMock):
		errorException = Exception("error")
		urlOpenMock.side_effect = errorException
		# -------------------------------------------------------
		self.apiService.getData()
		# -------------------------------------------------------
		self.assertEquals(self.apiService.failResult, errorException)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
