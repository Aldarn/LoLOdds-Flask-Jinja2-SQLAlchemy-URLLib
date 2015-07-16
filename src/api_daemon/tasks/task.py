import abc

class Task(object):
	__metaclass__ = abc.ABCMeta # This is an abstract base class and shouldn't be instantiated

	"""
	Runs the task.
	"""
	@abc.abstractmethod
	def run(self, *args, **kwargs):
		pass

	"""
	Saves the output of the task.
	"""
	@abc.abstractmethod
	def save(self, *args, **kwargs):
		pass
