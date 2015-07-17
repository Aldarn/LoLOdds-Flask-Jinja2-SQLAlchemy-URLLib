from src.hextech_project_x import DB

# *** NOTE:
#
# This should contain team_id and champion_id, however Flask-SQLAlchemy appears not to support
# "Associated" tables, or at least it is buggy. After several hours of trying to fix this i'm forced due to
# the remaining time to hack this into the Summoners table instead.

GAME_SUMMONERS = DB.Table(
	'game_summoners',
    DB.Column('game_id', DB.BigInteger, DB.ForeignKey('games.gameId'), primary_key = True),
    DB.Column('summoner_id', DB.BigInteger, DB.ForeignKey('summoners.summonerId'), primary_key = True)
)