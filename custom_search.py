from utils import Utils
from googleapiclient.discovery import build

class Custom_Search:

	cse_id = 'XXXXX'
	api_id = 'XXXXX'

	@classmethod
	def search(cls, search_term):
		result = 'xxttyy '

		service = build('customsearch', 'v1', developerKey = Custom_Search.api_id)
		metadata = service.cse().list(q = search_term, cx = Custom_Search.cse_id, num = 10).execute()

		try:
			data = metadata['items']
		except KeyError:
			print(f'CSE found no results for {search_term}')
			data = ''
		
		for item in data:
			result += item['title']
			result += ' '

			result += item['snippet']
			result += ' '

		result += 'xxttyy'

		return Utils.format_text(result)
