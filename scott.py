from question import Question
from utils import Utils
from custom_search import Custom_Search
import nat_lang
import wiki_search
import bing_search
from threading import Thread

class Scott:

	def __init__(self, vector, question, answers):
		self.vector = vector
		self.question = Question(question)
		self.raw_answers = answers
		self.answers = [Utils.format_text(st) for st in answers]

		self.text_dict = {'q_text': '', 'a1_text': '', 'a2_text': '', 'a3_text': '', 'wiki1_text': '', 'wiki2_text': '', 'wiki3_text': '', 'bing1_text': '', 'bing2_text': '', 'bing3_text': ''}
		self.answer_dict = {'qtext_ans': [0, 0, 0], 'atext_ans': [0, 0, 0], 'wiki_ans': [0, 0, 0], 'bing_ans': [0, 0, 0], 'atext_wiki_vec_ans': [0, 0, 0], 'bing_qtext_vec_ans': [0, 0, 0], 'wiki_vec_ans': [0, 0, 0], 'bingwiki_vec_ans': [0, 0, 0], 'vec_qa_text_ans': [0, 0, 0], 'vec_qa_words_ans': [0, 0, 0]}
		self.raw_answer_dict = {'qtext_ans': [0, 0, 0], 'atext_ans': [0, 0, 0], 'wiki_ans': [0, 0, 0], 'bing_ans': [0, 0, 0], 'atext_wiki_vec_ans': [0, 0, 0], 'bing_qtext_vec_ans': [0, 0, 0], 'wiki_vec_ans': [0, 0, 0], 'bingwiki_vec_ans': [0, 0, 0], 'vec_qa_text_ans': [0, 0, 0], 'vec_qa_words_ans': [0, 0, 0]}


	def get_text_threads(self):
		threads = []

		process = Thread(target = self.get_qtext)
		process.start()
		threads.append(process)

		for i in range(1, 4):
			process = Thread(target = self.get_wiki_text, args = [i])
			process.start()
			threads.append(process)

			process = Thread(target = self.get_bing_text, args = [i])
			process.start()
			threads.append(process)

			process = Thread(target = self.get_atext, args = [i])
			process.start()
			threads.append(process)

		for process in threads:
			process.join()

	def get_answer_threads(self):
		threads = []

		process = Thread(target = self.get_vec_qatext_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_vec_qawords_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_vec_wiki_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_vec_wiki_atext)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_vec_qtext_bing)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_vec_bingwiki_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_wiki_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_bing_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_q_ans)
		process.start()
		threads.append(process)

		process = Thread(target = self.get_a_ans)
		process.start()
		threads.append(process)

		for process in threads:
			process.join()

	def get_qtext(self):
		text = Custom_Search.search(self.question.text)

		self.text_dict['q_text'] = text

	def get_atext(self, ans_num):
		text = Custom_Search.search(self.question.text + ' ' + self.answers[ans_num - 1])

		self.text_dict[f'a{ans_num}_text'] = text

	def get_wiki_text(self, ans_num):
		try:
			words = ' '.join(nat_lang.get_entities(self.question.raw_text))
			if len(words) == 0:
				words = words = ' '.join(self.question.words)
			words = f'{words} {self.answers[ans_num - 1]}'

			titles = wiki_search.get_titles(words)
			text = wiki_search.get_text(titles[0])

		except IndexError:
			text = ''

		self.text_dict[f'wiki{ans_num}_text'] = text

	def get_bing_text(self,ans_num):
		text = bing_search.search(self.question.text + ' ' + self.answers[ans_num - 1])

		self.text_dict[f'bing{ans_num}_text'] = text

	def get_q_ans(self):
		results = []

		for ans_num in range(3):
			aterms = [wrd for wrd in self.answers[ans_num] if wrd not in self.question.words]
			count = self.text_matcher(self.text_dict['q_text'].split(), [], aterms)
			results.append(count)

		self.compute_ans_probs(results, 'qtext_ans')

	def get_a_ans(self):
		results = []
		qterms = self.question.words

		for ans_num in range(3):
			aterms = [wrd for wrd in self.answers[ans_num] if wrd not in qterms]
			count = self.text_matcher(self.text_dict[f'a{ans_num + 1}_text'].split(), qterms, aterms)
			results.append(count)

		self.compute_ans_probs(results, 'atext_ans')

	def get_wiki_ans(self):
		results = []
		qterms = self.question.words

		for ans_num in range(3):
			aterms = [wrd for wrd in self.answers[ans_num] if wrd not in qterms]
			count = self.text_matcher(self.text_dict[f'wiki{ans_num + 1}_text'].split(), qterms, aterms)
			results.append(count)

		self.compute_ans_probs(results, 'wiki_ans')

	def get_bing_ans(self):
		results = []
		qterms = self.question.words

		for ans_num in range(3):
			aterms = [wrd for wrd in self.answers[ans_num] if wrd not in qterms]
			count = self.text_matcher(self.text_dict[f'bing{ans_num + 1}_text'].split(), qterms, aterms)
			results.append(count)

		self.compute_ans_probs(results, 'bing_ans')

	def get_vec_wiki_atext(self):
		text = []
		keys = list(self.text_dict.keys())[1:7]
		for elem in keys:
			text.append(self.text_dict[elem])

		results = self.vector.compare_atext_wiki(text)

		self.compute_ans_probs(results, 'atext_wiki_vec_ans')

	def get_vec_qtext_bing(self):
		text = [self.text_dict['q_text'], self.text_dict['bing1_text'], self.text_dict['bing2_text'], self.text_dict['bing3_text']]

		results = self.vector.compare_bing_qtext(text)

		self.compute_ans_probs(results, 'bing_qtext_vec_ans')

	def get_vec_bingwiki_ans(self):
		text = []
		keys = list(self.text_dict.keys())[4:]
		for elem in keys:
			text.append(self.text_dict[elem])

		results = self.vector.compare_bing_wiki(text)

		self.compute_ans_probs(results, 'bingwiki_vec_ans')

	def get_vec_wiki_ans(self):
		text = [self.text_dict['wiki1_text'], self.text_dict['wiki2_text'], self.text_dict['wiki3_text']]

		results = self.vector.compare_ques_ans_wiki(text, self.question.text, self.answers)

		self.compute_ans_probs(results, 'wiki_vec_ans')

	def get_vec_qatext_ans(self):
		text = [self.text_dict['q_text'], self.text_dict['a1_text'], self.text_dict['a2_text'], self.text_dict['a3_text']]

		results = self.vector.compare_ques_ans_text(text)

		self.compute_ans_probs(results, 'vec_qa_text_ans')

	def get_vec_qawords_ans(self):
		text = [self.text_dict['q_text']]

		results = self.vector.compare_ques_ans_words(text, self.answers)

		self.compute_ans_probs(results, 'vec_qa_words_ans')

	def get_vec_atext_ans(self):
		text = [self.text_dict['a1_text'], self.text_dict['a2_text'], self.text_dict['a3_text']]

		results = self.vector.compare_ans_text(text)

		self.compute_ans_probs(results, 'vec_atext_ans')

	def compute_ans_probs(self, results, method):
		self.raw_answer_dict[method] = results

		total = sum(results)
		if total == 0:
			self.answer_dict[method] = results

		else:
			probs = []
			for elem in results:
				raw = elem/total
				perc = int((raw * 1000) + 0.5) / 1000.0
				probs.append(perc)

			self.answer_dict[method] = probs

	def text_matcher(self, text, qterms, aterms):
		try:
			q_step = 1/len(qterms)
		except ZeroDivisionError:
			q_step = 0

		a_step = 1/len(aterms)
		ind, count = 0, 0

		while ind < len(text):
			a_count, q_count = 0, 0
			lastword = ''

			while (ind < len(text)) and (text[ind] in qterms or text[ind] in aterms) and (text[ind] != lastword):
				if text[ind] in qterms:
					q_count += q_step
					lastword = text[ind]
					ind += 1

				elif text[ind] in aterms:
					a_count += a_step
					lastword = text[ind]
					ind += 1

			temp_count = a_count + q_count

			if temp_count > 1:
				const = (temp_count - 1)/2
			else:
				const = 0

			multiplier = 1 + const
			if a_count != 0 and q_count != 0:
				multiplier *= 2

			count += temp_count * multiplier

			if a_count == 0 and q_count == 0:
				ind += 1

		return count

	def naive_answer(self):
		probs = [0, 0, 0]
		for key in self.answer_dict:
			for i, prob in enumerate(self.answer_dict[key]):
				probs[i] += prob

		if self.question._not:
			return probs.index(min(probs)) + 1
		else:
			return probs.index(max(probs)) + 1

	def naive_answer_array(self, answers):
		if answers[len(answers) - 1] == 1:
			not_ques = True
		else:
			not_ques = False
		answers = answers[:len(answers) - 1]
		probs = [0, 0, 0]

		for i, elem in enumerate(answers):
			probs[i%3] += elem

		if not_ques:
			return probs.index(min(probs)) + 1
		else:
			return probs.index(max(probs)) + 1

	def answer_dict_array(self, methods=None):
		if methods == None:
			methods = self.answer_dict.keys()

		results = []
		for key in methods:
			for elem in self.answer_dict[key]:
				results.append(elem)

		if self.question._not:
			results.append(1)
		else:
			results.append(0)

		return results
