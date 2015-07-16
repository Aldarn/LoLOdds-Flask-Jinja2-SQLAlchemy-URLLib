from task import Task
from src.hextech_project_x import DB

class ProcessSummonerChampionTask(Task):
	def __init__(self, summoner):
		self.summoner = summoner

	def run(self):
		pass

	def save(self, summonerChampion, summoner):
		summoner.children.append(summonerChampion)
		DB.session.add(summonerChampion)
		DB.session.commit()
