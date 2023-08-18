from utils import Utils

class Question:

	def __init__(self, question):
		self._not = ' NOT ' in question
		self.text = Utils.format_text(question)
		self.words = self.text.split()
		self.raw_text = question