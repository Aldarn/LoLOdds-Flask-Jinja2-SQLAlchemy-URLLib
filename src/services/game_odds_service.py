class GameOddsService(object):
	def __init__(self):
		pass

	def getGamesWithOdds(self):
		return {
			"games": [
				{
					"summoners": [
						{
							"name": "yo"
						},
						{
							"name": "yo2"
						},
					]
				},
				{
					"summoners": [
						{
							"name": "hey"
						},
						{
							"name": "sup"
						},
					]
				}
			]
		}

GAME_ODDS_SERVICE = GameOddsService()
