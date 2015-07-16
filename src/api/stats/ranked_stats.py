from src.api.api_service import APIService

class RankedStats(APIService):
	ENDPOINT_BASE = "https://euw.api.pvp.net/api/lol/euw/v1.3/stats/by-summoner/"
	ENDPOINT = "/ranked"

	VALID_SEASONS = ("SEASON3", "SEASON2014", "SEASON2015")

	def __init__(self):
		super(RankedStats, self).__init__(RankedStats.ENDPOINT_BASE)

	def getStats(self, summonerId, season = None):
		if season and season in RankedStats.VALID_SEASONS:
			return self._getData(endpoint = "%s%s" % (summonerId, RankedStats.ENDPOINT), season = season)
		else:
			# Use the default if no season is provided
			return self._getData(endpoint = "%s%s" % (summonerId, RankedStats.ENDPOINT))

# Create a handle to this service
RANKED_STATS = RankedStats()
