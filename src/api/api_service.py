import abc
import src.resources.config as config
import urllib2
import json

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
		url = "%s&%s" % (self._getEndpointUrl(endpoint), '&'.join('%s=%s' % (key, value) for key, value in params.iteritems()))

		try:
			# Fetch the data and load it into a dictionary
			result = json.loads(urllib2.urlopen(url).read())

			# If the result has a status and status code that isn't 200, it failed
			if "status" in result and "status_code" in result["status"] and result["status"]["status_code"] != 200:
				self._onFail(result)
			# Anything else should be success
			else:
				self._onSuccess(result)
		except Exception, e:
			# TODO: Log error properly
			print "Failed to get API data: %s" % e
			self._onFail(e)

	"""
	Callback when data is grabbed successfully.
	"""
	@abc.abstractmethod
	def _onSuccess(self, result):
		pass

	"""
	Callback when grabbing data fails.
	"""
	@abc.abstractmethod
	def _onFail(self, result):
		pass
