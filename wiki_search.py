import requests
from utils import Utils

URL = 'http://en.wikipedia.org/w/api.php?'

def get_titles(text):
	params = {'prop': 'extracts', 'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': text}
	results = requests.get(URL, params).json()
	try:
		pages = results['query']['search']
	except Exception:
		print(results)

	titles = []
	for item in pages:
		titles.append(item['title'])

	return titles

def get_text(title):
	params = {'prop': 'extracts', 'action': 'query', 'format': 'json', 'pagelang': 'English', 'titles': title, 'explaintext': ''}
	results = requests.get(URL, params).json()

	pages = results['query']['pages']
	pageid = list(pages.keys())[0]
	text = pages[pageid]['extract']

	return Utils.format_text(text)
