from src.hextech_project_x import DB

"""
Represents an individual game.
"""
class Games(DB.Model):
	gameId = DB.Column(DB.BigInteger, primary_key = True, autoincrement = False)
	gameMode = DB.Column(DB.String(50), index = True)
	gameQueueId = DB.Column(DB.Integer, index = True)
	gameType = DB.Column(DB.String(50), index = True)
	mapId = DB.Column(DB.Integer, index = True)
	platformId = DB.Column(DB.String(10), index = True)

	summoners = DB.relationship('GameSummoners', backref = DB.backref('Games', lazy='joined'), lazy='dynamic')

	def __init__(self, gameId, gameMode, gameQueueId, gameType, mapId, platformId):
		self.gameId = gameId
		self.gameMode = gameMode
		self.gameQueueId = gameQueueId
		self.gameType = gameType
		self.mapId = mapId
		self.platformId = platformId

	def __repr__(self):
		return '<Game %i>' % self.gameId
