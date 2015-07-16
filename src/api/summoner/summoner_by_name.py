from src.api.api_service import APIService

class SummonerByName(APIService):
	ENDPOINT_BASE = "https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"

	def __init__(self):
		super(SummonerByName, self).__init__(SummonerByName.ENDPOINT_BASE)

	def getSummoner(self, summonerName):
		# Ensure all ids are converted to string format and then join them for the endpoint
		self._getData(endpoint = summonerName)

# Create a handle to this service
SUMMONER_BY_NAME = SummonerByName()
