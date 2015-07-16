import abc
import src.resources.config as config
import urllib2
import urllib
import json
import time

class APIService(object):
	__metaclass__ = abc.ABCMeta # This is an abstract base class and shouldn't be instantiated

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
		url = "%s&%s" % (self._getEndpointUrl(urllib2.quote(endpoint)), urllib.urlencode(params))
		print "api url: %s" % url
		try:
			# Fetch the data and load it into a dictionary
			result = json.loads(urllib2.urlopen(url).read())

			# If the result has a status and status code that isn't 200, it failed
			if "status" in result and "status_code" in result["status"] and result["status"]["status_code"] != 200:
				return False, result
			# Anything else should be success
			else:
				return True, result
		except urllib2.HTTPError, he:
			# Code 429 is rate limit, sleep it off and try again
			if he.code == 429:
				print "hit rate limit, sleeping..."
				time.sleep(config.RATE_LIMIT_TIMEOUT)
				return self._getData(endpoint = endpoint, **params)
			return False, he
		except Exception, e:
			# TODO: Log error properly
			print "Failed to get API data: %s" % e
			return False, e
