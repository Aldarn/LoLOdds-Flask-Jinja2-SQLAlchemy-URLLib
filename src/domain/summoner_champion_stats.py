from src.hextech_project_x import DB

"""
Records current champion ranked stats for a summoner. Each summoner will have an entry in this table
for each champion they have played a ranked game with.
"""
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
