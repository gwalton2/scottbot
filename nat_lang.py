from google.cloud import language
from google.cloud.language import types
from google.cloud.language import enums
import os
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'scott_key.json'
client = language.LanguageServiceClient()

def get_entities(text):
	document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
	entities = client.analyze_entities(document).entities

	words = []
	for entity in entities:
		words.append(entity.name)
	
	return words

def get_syntax(text):
	document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
	tokens = client.analyze_syntax(document).tokens

	pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
	words = []
	for token in tokens:
		tag = pos_tag[token.part_of_speech.tag]
		if tag == 'NOUN' or tag == 'ADJ':
			words.append(token.text.content)

	return words

