from src.domain.games import Games
import math
from fractions import gcd

class GameOddsService(object):
	def __init__(self):
		pass

	# def getGamesWithOdds(self):
	# 	return {
	# 		"games": [
	# 			{
	# 				"summoners": [
	# 					{
	# 						"name": "yo"
	# 					},
	# 					{
	# 						"name": "yo2"
	# 					},
	# 				]
	# 			},
	# 			{
	# 				"summoners": [
	# 					{
	# 						"name": "hey"
	# 					},
	# 					{
	# 						"name": "sup"
	# 					},
	# 				]
	# 			}
	# 		]
	# 	}

	# def getGamesWithOdds(self):
	# 	games = Games.query.all()
	#
	# 	gameList = []
	# 	for game in games:
	# 		summonersList = []
	# 		teamWinsAndLosses = {}
	# 		for summoner in game.summoners:
	# 			summonersList.append({
	# 				"name": summoner.name,
	# 				"championImageUrl": thingy
	# 			})
	# 		gameList.append({ "summoners": summonersList })
	#
	# 	return { "games": gameList }

	def _calculateGameOdds(self, redTotalWins, redTotalLosses, purpleTotalWins, purpleTotalLosses):
		redWinPercentage = self._getPercentage(redTotalWins, redTotalLosses)
		purpleWinPercentage = self._getPercentage(purpleTotalWins, purpleTotalLosses)

		redChance = self._getPercentage(redWinPercentage, purpleWinPercentage)
		purpleChance = self._getPercentage(purpleWinPercentage, redWinPercentage)

		greatestCommonDivider = gcd(redChance, purpleChance)

		return "%i : %i" % (redChance / greatestCommonDivider, purpleChance / greatestCommonDivider)

	def _getPercentage(self, i1, i2):
		return math.floor((i1 / (i1 + i2)) * 100)

GAME_ODDS_SERVICE = GameOddsService()
