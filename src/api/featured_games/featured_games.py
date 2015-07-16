from src.api.api_service import APIService

class FeaturedGames(APIService):
	def __init__(self):
		super(FeaturedGames, self).__init__("https://euw.api.pvp.net/observer-mode/rest/featured")

	def getFeaturedGames(self):
		return self._getData()

# Create a handle to this service
FEATURED_GAMES = FeaturedGames()