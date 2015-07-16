from src.hextech_project_x import DB

GAME_SUMMONERS = DB.Table(
	'game_summoners',
    DB.Column('game_id', DB.BigInteger, DB.ForeignKey('games.gameId'), primary_key = True),
    DB.Column('summoner_id', DB.BigInteger, DB.ForeignKey('summoners.summonerId'), primary_key = True)
)