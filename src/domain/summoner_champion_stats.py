from src.hextech_project_x import DB

class SummonerChampionStats(DB.Model):
	summonerId = DB.Column(DB.Integer, primary_key = True, autoincrement = False)
	championId = DB.Column(DB.Integer, primary_key = True, autoincrement = False)
	championImageUrl = DB.Column(DB.String(255)) # This really really shouldn't be here as it will be duplicated for all summoners (amongst other reasons)
	totalSessionsWon = DB.Column(DB.Integer)
	totalSessionsLost = DB.Column(DB.Integer)

	def __init__(self, summonerId, championId, championImageUrl, totalSessionsWon, totalSessionsLost):
		self.summonerId = summonerId
		self.championId = championId
		self.championImageUrl = championImageUrl
		self.totalSessionsWon = totalSessionsWon
		self.totalSessionsLost = totalSessionsLost

	def __repr__(self):
		return '<Summoner Champion Stats %i, %i>' % (self.summonerId, self.championId)
