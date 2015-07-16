from src.hextech_project_x import DB

class Game(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	gameId = DB.Column(DB.Integer, unique=True)
	gameMode = DB.Column(DB.String(50))
	gameQueueId = DB.Column(DB.Integer)
	gameType = DB.Column(DB.String(50))
	mapId = DB.Column(DB.Integer)
	platformId = DB.Column(DB.Integer)

	def __init__(self, gameId, gameMode, gameQueueId, gameType, mapId, platformId):
		self.gameId = gameId
		self.gameMode = gameMode
		self.gameQueueId = gameQueueId
		self.gameType = gameType
		self.mapId = mapId
		self.platformId = platformId

	def __repr__(self):
		return '<Game %i>' % self.gameId
