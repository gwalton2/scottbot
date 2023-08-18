import re

class Utils:

	@classmethod
	def format_text(cls, text):
		remove_words = ['which', 'not', 'these', 'in', 'on', 'and', 'of', 'the', 'that', 'an', 'to']
		result = text.lower()
		result = re.sub('[\n]', ' ', result)
		result = re.sub('[-—]', ' ', result)
		result = re.sub('[^\w\s]', '', result)

		word_list = result.split()
		return ' '.join([st for st in word_list if st not in remove_words])
