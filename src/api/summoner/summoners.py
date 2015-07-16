from src.api.api_service import APIService

class Summoners(APIService):
	ENDPOINT_BASE = "https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/"

	def __init__(self):
		super(Summoners, self).__init__(Summoners.ENDPOINT_BASE)

	def getSummoners(self, summonerIds):
		# Ensure all ids are converted to string format and then join them for the endpoint
		self._getData(','.join(map(lambda summonerId: str(summonerId), summonerIds)))

	def _onSuccess(self, result):
		pass

	def _onFail(self, result):
		pass

# Create a handle to this service
SUMMONERS = Summoners()
