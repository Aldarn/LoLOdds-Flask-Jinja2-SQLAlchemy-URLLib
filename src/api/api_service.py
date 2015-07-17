import abc
import src.resources.config as config
import urllib2
import urllib
import json
import time

class APIService(object):
	__metaclass__ = abc.ABCMeta # This is an abstract base class and shouldn't be instantiated

	RATE_LIMIT_HTTP_CODE = 429
	SERVICE_UNAVAILABLE_CODE = 503
	GATEWAY_TIMEOUT_CODE = 504
	NO_INTERNET_ERROR_CODES = ["Errno 50", "Errno 8", "Errno 60"]

	def __init__(self, endpointBase):
		self._apiEndpointBase = endpointBase

	"""
	Appends the API key onto the given endpoint.
	"""
	def _getEndpointUrl(self, endpoint = ""):
		return "%s%s?api_key=%s" % (self._apiEndpointBase, endpoint, config.API_KEY)

	"""
	Gets the data at the given endpoint.
	"""
	def _getData(self, endpoint = "", **params):
		# Combine any parameters with the endpoint url
		url = "%s&%s" % (self._getEndpointUrl(endpoint), urllib.urlencode(params))
		print "api url: %s" % url
		try:
			# Fetch the data and load it into a dictionary
			result = json.loads(urllib2.urlopen(url).read())

			# If the result has a status and status code that isn't 200, it failed
			if "status" in result and "status_code" in result["status"] and result["status"]["status_code"] != 200:
				return self.__handleError(result)
			# Anything else should be success
			else:
				return True, result

		except urllib2.HTTPError, he:
			# Code 429 is rate limit, sleep it off and try again
			# TODO: Handling this here maybe isn't the best idea if some service wants to react differently,
			# but for now it's ok - YAGNI and all that
			if he.code == APIService.RATE_LIMIT_HTTP_CODE:
				print "hit rate limit, sleeping..."
				time.sleep(config.RATE_LIMIT_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			elif he.code == APIService.SERVICE_UNAVAILABLE_CODE:
				print "service unavailable, sleeping..."
				time.sleep(config.SERVICE_UNAVAILABLE_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			elif he.code == APIService.GATEWAY_TIMEOUT_CODE:
				print "gateway timeout, sleeping..."
				time.sleep(config.GATEWAY_TIMEOUT_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			return self.__handleError(he)

		except urllib2.URLError, urle:
			# Handle cases of an internet connection drop
			# I wish there was a nicer way to get this, but looking at the API it doesn't look like it's exposed
			if any(noInternetErrorCode in urle.__str__() for noInternetErrorCode in APIService.NO_INTERNET_ERROR_CODES):
				print "internet has died, sleeping..."
				time.sleep(config.NO_INTERNET_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			return self.__handleError(urle)

		except Exception, e:
			return self.__handleError(e)

	def __handleError(self, e):
		# TODO: Log error properly
		print "Failed to get API data: %s" % e
		return False, e