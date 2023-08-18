from gensim.models import Doc2Vec
import numpy as np

class Vector:

	def __init__(self):
		self.model = Doc2Vec.load('./imdb.d2v')

	def compare_atext_wiki(self, text):
		a1_vec = self.model.infer_vector(text[0].split())
		a2_vec = self.model.infer_vector(text[1].split())
		a3_vec = self.model.infer_vector(text[2].split())

		wiki1_vec = self.model.infer_vector(text[3].split())
		wiki2_vec = self.model.infer_vector(text[4].split())
		wiki3_vec = self.model.infer_vector(text[5].split())

		return [self.cosine_sim(wiki1_vec, a1_vec), self.cosine_sim(wiki2_vec, a2_vec), self.cosine_sim(wiki3_vec, a3_vec)]

	def compare_bing_wiki(self, text):
		wiki1_vec = self.model.infer_vector(text[0].split())
		wiki2_vec = self.model.infer_vector(text[1].split())
		wiki3_vec = self.model.infer_vector(text[2].split())
		
		bing1_vec = self.model.infer_vector(text[3].split())
		bing2_vec = self.model.infer_vector(text[4].split())
		bing3_vec = self.model.infer_vector(text[5].split())

		return [self.cosine_sim(wiki1_vec, bing1_vec), self.cosine_sim(wiki2_vec, bing2_vec), self.cosine_sim(wiki3_vec, bing3_vec)]

	def compare_bing_qtext(self, text):
		q_vec = self.model.infer_vector(text[0].split())

		bing1_vec = self.model.infer_vector(text[1].split())
		bing2_vec = self.model.infer_vector(text[2].split())
		bing3_vec = self.model.infer_vector(text[3].split())

		return [self.cosine_sim(q_vec, bing1_vec), self.cosine_sim(q_vec, bing2_vec), self.cosine_sim(q_vec, bing3_vec)]

	def compare_ques_ans_wiki(self, text, question, answers):
		wiki1_vec = self.model.infer_vector(text[0].split())
		wiki2_vec = self.model.infer_vector(text[1].split())
		wiki3_vec = self.model.infer_vector(text[2].split())
		
		a1_vec = self.model.infer_vector(f'{question} {answers[0]}')
		a2_vec = self.model.infer_vector(f'{question} {answers[1]}')
		a3_vec = self.model.infer_vector(f'{question} {answers[2]}')

		return [self.cosine_sim(wiki1_vec, a1_vec), self.cosine_sim(wiki2_vec, a2_vec), self.cosine_sim(wiki3_vec, a3_vec)]

	def compare_ques_ans_text(self, text):
		q_vec = self.model.infer_vector(text[0].split())

		a1_vec = self.model.infer_vector(text[1].split())
		a2_vec = self.model.infer_vector(text[2].split())
		a3_vec = self.model.infer_vector(text[3].split())

		return [self.cosine_sim(q_vec, a1_vec), self.cosine_sim(q_vec, a2_vec), self.cosine_sim(q_vec, a3_vec)]

	def compare_ques_ans_words(self, text, answers):
		q_vec = self.model.infer_vector(text[0].split())

		a1_vec = self.model.infer_vector(answers[0])
		a2_vec = self.model.infer_vector(answers[1])
		a3_vec = self.model.infer_vector(answers[2])

		return [self.cosine_sim(q_vec, a1_vec), self.cosine_sim(q_vec, a2_vec), self.cosine_sim(q_vec, a3_vec)]

	def compare_ans_text(self, text):
		a1_vec = self.model.infer_vector(text[0])
		a2_vec = self.model.infer_vector(text[1])
		a3_vec = self.model.infer_vector(text[2])

		return [self.cosine_sim(a2_vec, a3_vec), self.cosine_sim(a1_vec, a3_vec), self.cosine_sim(a1_vec, a2_vec)]


	def cosine_sim(self, v1, v2):
		dot_prod = np.dot(v1, v2)

		norm_1 = np.linalg.norm(v1)
		norm_2 = np.linalg.norm(v2)

		return dot_prod/(norm_1 * norm_2)
