import time
import json

class Save_Json:

	def __init__(self, game_time):
		self.game_time = game_time
		self.data = {game_time: {}}

	def add(self, entry, newdata):
		self.data[self.game_time][entry] = newdata

	def append(self, newdata, filename):
		with open(filename, mode='r', encoding='utf-8') as file:
			feed = json.load(file)

		with open(filename, mode='w', encoding='utf-8') as file:
			feed.append(newdata)
			json.dump(feed, file)

	def save(self, filename):
		with open(filename, mode='r', encoding='utf-8') as file:
			feed = json.load(file)

		with open(filename, mode='w', encoding='utf-8') as file:
			feed.append(self.data)
			json.dump(feed, file)