from src.api.api_service import APIService
import re

class SummonerByName(APIService):
	ENDPOINT_BASE = "https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"

	def __init__(self):
		super(SummonerByName, self).__init__(SummonerByName.ENDPOINT_BASE)

	def getSummoner(self, summonerName):
		# Ensure all ids are converted to string format and then join them for the endpoint
		summonerName = self._getAPIFriendlySummonerName(summonerName)
		print "getting summoner %s" % summonerName
		return self._getData(endpoint = summonerName)

	"""
	Converts the summoner name into the encoding expected by the RIOT API that also doesn't
	upset HTTP.
	"""
	def _getAPIFriendlySummonerName(self, summonerName):
		return self._urlEncodeNonAscii(summonerName.encode('utf-8')).lower().replace(' ', '')

	"""
	Encodes non-ascii characters for HTTP.
	"""
	def _urlEncodeNonAscii(self, b):
		return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

# Create a handle to this service
SUMMONER_BY_NAME = SummonerByName()
