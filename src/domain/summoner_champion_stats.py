from src.hextech_project_x import DB

class SummonerChampionStats(DB.Model):
	summonerId = DB.Column(DB.BigInteger, DB.ForeignKey('summoners.summonerId'), primary_key = True, autoincrement = False)
	championId = DB.Column(DB.BigInteger, primary_key = True, autoincrement = False)
	totalSessionsWon = DB.Column(DB.Integer)
	totalSessionsLost = DB.Column(DB.Integer)

	def __init__(self, summonerId, championId, totalSessionsWon, totalSessionsLost):
		self.summonerId = summonerId
		self.championId = championId
		self.totalSessionsWon = totalSessionsWon
		self.totalSessionsLost = totalSessionsLost

	def __repr__(self):
		return '<Summoner Champion Stats %i, %i>' % (self.summonerId, self.championId)
