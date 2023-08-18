import requests
from utils import Utils

sub_key = 'XXXXX'
search_url = 'XXXXX'
headers = {"Ocp-Apim-Subscription-Key" : sub_key}

def search(search_term):
	params  = {'q': search_term}

	response = requests.get(search_url, headers=headers, params=params)
	if response.status_code != 200:
		print(f'Error with Bing_Search: {search_term}')
	metadata = response.json()

	try:
		data = metadata['webPages']['value']
	except KeyError:
		print(f'Bing found no results for {search_term}')
		data = ''

	result = 'xxttyy '
	for item in data:
		result += item['name']
		result += ' '

		result += item['snippet']
		result += ' '

	result += 'xxttyy'

	return Utils.format_text(result)
	
