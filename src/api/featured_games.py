from src.api.api_service import APIService

class FeaturedGames(APIService):
	def __init__(self):
		super(FeaturedGames, self).__init__("https://euw.api.pvp.net/observer-mode/rest/featured")

	def _onSuccess(self, result):
		pass

	def _onFail(self, result):
		pass