from task import Task
from src.hextech_project_x import DB

class ProcessParticipantTask(Task):
	def __init__(self, participantName, game):
		self.participantName = participantName
		self.game = game

	def run(self):
		pass

	def save(self, summoner, game):
		game.children.append(summoner)
		DB.session.add(summoner)
		DB.session.commit()
