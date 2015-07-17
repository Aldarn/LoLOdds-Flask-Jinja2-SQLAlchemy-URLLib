from src.hextech_project_x import DB

class Summoners(DB.Model):
	summonerId = DB.Column(DB.BigInteger, primary_key = True, autoincrement = False)
	name = DB.Column(DB.Unicode(100, collation='utf8mb4_unicode_ci'), index = True)
	platformId = DB.Column(DB.String(10), index = True)
	iconImageUrl = DB.Column(DB.String(255))
	lastModified = DB.Column(DB.BigInteger, index = True)
	lastStatsModified = DB.Column(DB.BigInteger, index = True)
	level = DB.Column(DB.Integer)
	totalSessionsWon = DB.Column(DB.Integer)
	totalSessionsLost = DB.Column(DB.Integer)
	teamId = DB.Column(DB.Integer) # TODO: This should be in the join table! *Raises pitchfork at SQLAlchemy*
	championId = DB.Column(DB.Integer) # TODO: This should be in the join table! *Raises pitchfork at SQLAlchemy*
	championImageUrl = DB.Column(DB.String(255)) # TODO: This should be stored in its own image table to prevent redundancy

	summonerChampionStats = DB.relationship('SummonerChampionStats',
        backref = DB.backref('Summoners', lazy='joined'), lazy='dynamic')

	def __init__(self, summonerId, name, iconImageUrl, lastModified, lastStatsModified, level, totalSessionsWon,
			totalSessionsLost, teamId, championId, championImageUrl):
		self.summonerId = summonerId
		self.name = name
		self.iconImageUrl = iconImageUrl
		self.lastModified = lastModified
		self.lastStatsModified = lastStatsModified
		self.level = level
		self.totalSessionsWon = totalSessionsWon
		self.totalSessionsLost = totalSessionsLost
		self.teamId = teamId
		self.championId = championId
		self.championImageUrl = championImageUrl

	def __repr__(self):
		return '<Summoner %i>' % self.summonerId
