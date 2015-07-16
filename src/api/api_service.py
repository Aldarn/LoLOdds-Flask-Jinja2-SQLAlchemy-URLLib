import abc
import src.resources.config as config
import urllib2
import json

class APIService(object):
	__metaclass__ = abc.ABCMeta # This is an abstract base class and shouldn't be instantiated

	def __init__(self, endpoint):
		self._apiEndpoint = endpoint

	"""
	Appends the API key onto the given endpoint
	"""
	def getEndpoint(self):
		return "%s?api_key=%s" % (self._apiEndpoint, config.API_KEY)

	"""
	Gets the data at the given endpoint
	"""
	def getData(self, **kwargs):
		# Combine any parameters with the endpoint url
		url = "%s%s" % (self.getEndpoint(), '&'.join('%s=%s' % (key, value) for key, value in kwargs.iteritems()))

		try:
			# Fetch the data and load it into a dictionary
			result = json.loads(urllib2.urlopen(url).read())

			# If the result has a status and status code that isn't 200, it failed
			if "status" in result and "status_code" in result["status"] and result["status"]["status_code"] != 200:
				self._onFail(result)
			# Anything else should be success
			else:
				self._onSuccess()
		except Exception, e:
			# TODO: Log error
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
