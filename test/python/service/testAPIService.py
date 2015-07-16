#!/usr/bin/env/python2.7

import unittest
from mock import patch, Mock, MagicMock
import src.resources.config as config
from src.api.api_service import APIService

class TestAPIService(unittest.TestCase):
	class TestAPIService(APIService):
		def __init__(self):
			super(TestAPIService.TestAPIService, self).__init__("bla.com/bla")

	def setUp(self):
		self.apiService = TestAPIService.TestAPIService()
		config.API_KEY = "testKey"

	def testGetEndpointCorrectFormat(self):
		# -------------------------------------------------------
		result = self.apiService._getEndpointUrl()
		# -------------------------------------------------------
		self.assertEquals(result, "bla.com/bla?api_key=testKey")

	def testGetEndpointWithEndpointCorrectFormat(self):
		# -------------------------------------------------------
		result = self.apiService._getEndpointUrl("/thingy/123/otherThingy")
		# -------------------------------------------------------
		self.assertEquals(result, "bla.com/bla/thingy/123/otherThingy?api_key=testKey")

	@patch('src.api.api_service.urllib2')
	def testGetDataParams(self, urllibMock):
		urllibMock.quote.side_effect = ['']
		# -------------------------------------------------------
		self.apiService._getData(thing = "sup")
		# -------------------------------------------------------
		urllibMock.urlopen.assert_called_with("bla.com/bla?api_key=testKey&thing=sup")

	@patch('src.api.api_service.urllib2')
	def testGetDataParamsWithEndpoint(self, urllibMock):
		urllibMock.quote.side_effect = ['/thingy/123/otherThingy']
		# -------------------------------------------------------
		self.apiService._getData(endpoint = "/thingy/123/otherThingy", thing = "sup")
		# -------------------------------------------------------
		urllibMock.urlopen.assert_called_with("bla.com/bla/thingy/123/otherThingy?api_key=testKey&thing=sup")

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataSuccess(self, urlOpenMock):
		urlOpenResponse = Mock()
		urlOpenResponse.read.side_effect = ['{"test": "yup"}']
		urlOpenMock.return_value = urlOpenResponse
		# -------------------------------------------------------
		success, data = self.apiService._getData()
		# -------------------------------------------------------
		self.assertTrue(success)
		self.assertEquals(data, {"test": "yup"})

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataFailCallsOnFail(self, urlOpenMock):
		urlOpenResponse = Mock()
		urlOpenResponse.read.side_effect = ['{"status": {"status_code": 404}}']
		urlOpenMock.return_value = urlOpenResponse
		# -------------------------------------------------------
		failure, data = self.apiService._getData()
		# -------------------------------------------------------
		self.assertFalse(failure)
		self.assertEquals(data, {"status": {"status_code": 404}})

	@patch('src.api.api_service.urllib2.urlopen')
	def testGetDataErrorCallsOnFail(self, urlOpenMock):
		errorException = Exception("error")
		urlOpenMock.side_effect = errorException
		# -------------------------------------------------------
		failure, exception = self.apiService._getData()
		# -------------------------------------------------------
		self.assertFalse(failure)
		self.assertEquals(exception, errorException)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
