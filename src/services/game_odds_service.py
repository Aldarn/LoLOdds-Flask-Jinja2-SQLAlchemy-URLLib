import math
from fractions import gcd
from collections import defaultdict

class GameOddsService(object):
	def __init__(self):
		pass

	def getGamesWithOdds(self):
		games = Games.query.all()

		gameList = []
		for game in games:
			summonersList = []
			teamWinsAndLosses = defaultdict(lambda: defaultdict(int))
			for summoner in game.summoners:
				teamWinsAndLosses[summoner.teamId]["wins"] += summoner.totalSessionsWon
				teamWinsAndLosses[summoner.teamId]["losses"] += summoner.totalSessionsLost
				summonersList.append({
					"name": summoner.name,
					"championImageUrl": summoner.championImageUrl,
					"winRate": self._getPercentage(summoner.totalSessionsWon, summoner.totalSessionsLost)
				})

			# There's probably a better way of doing this, but at 3am i'm happy...
			odds = self._calculateGameOdds(teamWinsAndLosses[teamWinsAndLosses.keys()[0]]["wins"],
				teamWinsAndLosses[teamWinsAndLosses.keys()[0]]["losses"],
				teamWinsAndLosses[teamWinsAndLosses.keys()[1]]["wins"],
				teamWinsAndLosses[teamWinsAndLosses.keys()[1]]["losses"])

			gameList.append({ "summoners": summonersList, "odds": odds })

		return { "games": gameList }

	def _calculateGameOdds(self, redTotalWins, redTotalLosses, purpleTotalWins, purpleTotalLosses):
		redWinPercentage = self._getPercentage(redTotalWins, redTotalLosses)
		purpleWinPercentage = self._getPercentage(purpleTotalWins, purpleTotalLosses)

		redChance = self._getPercentage(redWinPercentage, purpleWinPercentage)
		purpleChance = self._getPercentage(purpleWinPercentage, redWinPercentage)

		greatestCommonDivider = gcd(redChance, purpleChance)
		if greatestCommonDivider == 0:
			greatestCommonDivider = 1

		return "%i : %i" % (redChance / greatestCommonDivider, purpleChance / greatestCommonDivider)

	def _getPercentage(self, i1, i2):
		# In this context, if both values are 0 that means there's no data on wins or losses, so lets call
		# the chance of a win or loss 50/50
		if i1 == 0 and i2 == 0:
			return 50
		return math.floor((float(i1) / (i1 + i2)) * 100)

GAME_ODDS_SERVICE = GameOddsService()

from src.domain.games import Games
from src.domain.game_summoners import GAME_SUMMONERS
from src.domain.summoners import Summoners
from src.domain.summoner_champion_stats import SummonerChampionStats