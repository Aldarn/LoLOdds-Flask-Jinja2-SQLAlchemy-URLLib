#!/usr/bin/env/python2.7

# Must import all DB models / tables
from src.hextech_project_x import DB
from src.domain.games import Games
from src.domain.summoners import Summoners
from src.domain.game_summoners import GAME_SUMMONERS
from src.domain.summoner_champion_stats import SummonerChampionStats

# Create & commit them
DB.create_all()
DB.session.commit()