from src.hextech_project_x import DB

class Summoners(DB.Model):
	summonerId = DB.Column(DB.Integer, primary_key = True, autoincrement = False)
	name = DB.Column(DB.String(100))
	iconId = DB.Column(DB.Integer)
	lastModified = DB.Column(DB.Integer)
	level = DB.Column(DB.Integer)
	totalSessionsWon = DB.Column(DB.Integer)
	totalSessionsLost = DB.Column(DB.Integer)

	summonerChampionStats = DB.relationship('SummonerChampionStats',
        backref = DB.backref('summoners', lazy='joined'), lazy='dynamic')

	def __init__(self, summonerId, name, iconId, lastModified, level, totalSessionsWon, totalSessionsLost):
		self.summonerId = summonerId
		self.name = name
		self.iconId = iconId
		self.lastModified = lastModified
		self.level = level
		self.totalSessionsWon = totalSessionsWon
		self.totalSessionsLost = totalSessionsLost

	def __repr__(self):
		return '<Summoner %i>' % self.summonerId
