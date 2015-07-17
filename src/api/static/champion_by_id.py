from src.api.api_service import APIService

class ChampionById(APIService):
	ENDPOINT_BASE = "https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/"

	def __init__(self):
		super(ChampionById, self).__init__(ChampionById.ENDPOINT_BASE)

	def getChampion(self, championId):
		return self._getData(endpoint = championId)

	def getChampionImageName(self, championId):
		success, data = self._getData(endpoint = championId, champData = "image")
		if success:
			return data["image"]["full"]
		return success, data

# Create a handle to this service
CHAMPION_BY_ID = ChampionById()
