import abc
import src.resources.config as config
import urllib2
import urllib
import json
import time

class APIService(object):
	__metaclass__ = abc.ABCMeta # This is an abstract base class and shouldn't be instantiated

	# HTTP errors that should trigger a request retry after a short period
	# REQUEST_TIMEOUT, SERVICE_UNAVAILABLE & GATEWAY_TIMEOUT
	RETRY_REQUEST_HTTP_CODES = [408, 503, 504]

	# HTTP error code corresponding to hitting the RIOT API rate limit
	RATE_LIMIT_HTTP_CODE = 429

	# Error codes that occur within urllib when there's no internet
	# Technically the EOF one refers to an SSL error that happens randomly
	NO_INTERNET_ERROR_CODES = ["Errno 50", "Errno 8", "Errno 60", "EOF"]

	def __init__(self, endpointBase):
		self._apiEndpointBase = endpointBase

	"""
	Appends the API key onto the given endpoint.
	"""
	def _getEndpointUrl(self, endpoint = ""):
		return "%s%s?api_key=%s" % (self._apiEndpointBase, endpoint, config.API_KEY)

	"""
	Gets the data at the given endpoint.

	TODO: Consider refactoring this to use the python-requests library to make it a bit
	simpler and possibly improve handling different edge case errors.
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
			# TODO: Handling this here maybe isn't the best idea if some service wants to react differently,
			# but for now it's ok - YAGNI and all that
			if he.code == APIService.RATE_LIMIT_HTTP_CODE:
				print "hit rate limit, sleeping..."
				time.sleep(config.RATE_LIMIT_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			elif he.code in APIService.RETRY_REQUEST_HTTP_CODES:
				print "%s, sleeping..." % he.msg
				time.sleep(config.RETRY_REQUEST_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			return self.__handleError(he)

		except urllib2.URLError, urle:
			# Handle cases of an internet connection drop
			# I wish there was a nicer way to get this, but looking at the API it doesn't seem like it's exposed
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