#!/usr/bin/env python3



import os
import re
import nltk
import math
import json
import string
import configparser
from lxml import etree
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob as tb
from nltk.stem import WordNetLemmatizer




class GenericDataAnalyzer(object):


	def __init__(self, configuration):
		"""
		Blabla
		"""

		self.config = configparser.ConfigParser()
		self.config.read(configuration)

		self.base_directory = self.config.get('utilities', 'base_directory')
		self.file_list = os.listdir(self.base_directory)

		self.passed = 0

		self.stopwords = set(stopwords.words('french'))
		self.punctuation = set(string.punctuation)

		# DATA
		with open(self.config.get('utilities', 'french_words'), 'r') as myfile:
			self.french_words = [word.strip('\n') for word in myfile if len(word) > 2]
		with open(self.config.get('utilities', 'french_departements'), 'r') as myfile:
			self.departements = [word.strip('\n').lower() for word in myfile]
		with open(self.config.get('utilities', 'french_regions'), 'r') as myfile:
			self.regions = [word.strip('\n').lower() for word in myfile]


	def tf(self, word, blob):
		return blob.words.count(word) / len(blob.words)


	def n_containing(self, word, bloblist):
		return sum(1 for blob in bloblist if word in blob.words)


	def idf(self, word, bloblist):
		return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))


	def tfidf(self, word, blob, bloblist):
		return self.tf(word, blob) * self.idf(word, bloblist)


	def find_ngrams(self, input_list, n):

		""" 
		Easiest way to get nGrams 
		"""

		return list(zip(*[input_list[i:] for i in range(int(n))]))


	def compute_distance(self, word_1, word_2):
		""" Compute the Levensthein distance between two words """
		if len(word_1) > len(word_2):
			word_1, word_2 = word_2, word_1
		if len(word_2) == 0:
			return len(word_1)
		word_1_length = len(word_1) + 1
		word_2_length = len(word_2) + 1
		distance_matrix = [[0] * word_2_length for x in range(word_1_length)]
		for i in range(word_1_length):
		   distance_matrix[i][0] = i
		for j in range(word_2_length):
		   distance_matrix[0][j] = j
		for i in range(1, word_1_length):
			for j in range(1, word_2_length):
				deletion = distance_matrix[i-1][j] + 1
				insertion = distance_matrix[i][j-1] + 1
				substitution = distance_matrix[i-1][j-1]
				if word_1[i-1] != word_2[j-1]:
					substitution += 1
				distance_matrix[i][j] = min(insertion, deletion, substitution)

		return distance_matrix[word_1_length-1][word_2_length-1]


	def data_preprocessing(self):
		"""
		TEXT PREPROCESSING
		"""

		cleaned_data = []
		lemmatiser = WordNetLemmatizer()
		print('\nTraining on {} documents.'.format(self.config['options']['number_of_documents']))
		for infile in self.file_list:
			if re.search('BSV', infile) and re.search('txt', infile):
				document_details = {}
				with open(self.base_directory+infile, 'r') as myfile:
					print('\t- Processing: {}'.format(infile))
					# GET RAW DATA
					data = myfile.read().replace('\n', '').lower()
					document_details['raw'] = data
					# TOKENIZE AND GRAM
					tokenized_data = nltk.word_tokenize(data)
					#~ document_details['gram_2'] = [word for word in self.find_ngrams(input_list=tokenized_data, n=2)]
					#~ document_details['gram_3'] = [word for word in self.find_ngrams(input_list=tokenized_data, n=3)]
					# CLEAN AND LEMME TOKENS
					lemmed_data = []
					for word in tokenized_data:
						if len(word) > 2:
							# IF WORD OK AND WELL SPELLED
							if (word not in self.stopwords) and (word not in self.punctuation):
								if word in self.french_words:
									lemmed_data.append(lemmatiser.lemmatize(word))
								else:
									# IF THIS IS A WORD WITH PREFFIX
									if re.search('[\’\']', word):
										prefix_removed = re.findall('[a-z]{1,2}[\’\'](.*)', word)
										if len(prefix_removed) > 0:
											if (prefix_removed[0] not in self.stopwords) and (prefix_removed[0] not in self.punctuation):
												if prefix_removed[0] in self.french_words:
													lemmed_data.append(prefix_removed[0])
												# BAD ORTHOGRAPHE
												else:
													if self.config.getboolean('options', 'correct_ortho') is True:
														distance = 10
														for french_word in self.french_words:
															new_distance = self.compute_distance(word_1=french_word, word_2=prefix_removed[0])
															if new_distance < distance:
																print('\t\tCorrecting [{}]\tFound: [{}]  (d={})'.format(word, french_word, new_distance))
																distance = new_distance
																word_corrected = french_word
														lemmed_data.append(word_corrected)
													else:
														continue
									# OR A COMPOSED WORD SPLITTED ON TWO LINES
									elif re.search('[\-]', word):
										corrected_word = re.sub('-', '', word)
										if (corrected_word not in self.stopwords) and (corrected_word not in self.punctuation):
												if corrected_word in self.french_words:
													lemmed_data.append(corrected_word)
												# BAD ORTHOGRAPHE
												else:
													if self.config.getboolean('options', 'correct_ortho') is True:
														distance = 10
														for french_word in self.french_words:
															new_distance = self.compute_distance(word_1=french_word, word_2=corrected_word)
															if new_distance < distance:
																print('\t\tCorrecting [{}]\tFound: [{}]  (d={})'.format(word, french_word, new_distance))
																distance = new_distance
																word_corrected = french_word
														lemmed_data.append(word_corrected)
													else:
														continue
					# STORE
					document_details['lemmed_data'] = lemmed_data
					document_details['file_name'] = infile
					cleaned_data.append(document_details)
					self.passed += 1
				# STOP TRAINING IF THRESHOLD REACHED
				if self.passed == self.config.getint('options', 'number_of_documents'):
					break

		return cleaned_data


	def train_tfidf(self, data):
		"""
		Blabla
		"""

		# JOIN EVERY LEMMED TERMS IN A STR() FOR TEXTBLOB
		bloblist = []
		for extracted_document in data:
			bloblist.append(tb(' '.join(extracted_document['lemmed_data'])))
		# THEN, COMPUTE SCORES AND STOR THEM
		for indice in range(0, len(bloblist)):
			scores = {word: self.tfidf(word, bloblist[indice], bloblist) for word in bloblist[indice].words}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			data[indice]['scored_words'] = list(sorted_words)
		print('Model trained and words scored (TF-IDF).\n')
		# SAVE OR NOT
		if self.config.getboolean('options', 'save_model') is True:
			with open('tfidf_model.json', 'w') as model_file:
				model_file.write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

		return data


	def analyze(self, data):
		"""
		Blabla
		"""

		# SUMMARY PLOT
		if self.config.getboolean('options', 'plot_graphes') is True:
			pass
		# THEN, ANALYZE
		if self.config.getboolean('options', 'summarize_data') is True:
			for document in data:
				print('\n{}\t({} words scorred)\n\tTop 10 words:'.format(document['file_name'], len(document['scored_words'])))
				for word in document['scored_words'][:10]:
					print('\t\t- {}'.format(word))

		# TERMINOLOGY MAPPING
		print('\nTerminology mapping on you documents.')
		with open('./terminology/vegetal_french_terminology.xml', 'r') as my_terminology:
			termino_tree = etree.parse(my_terminology)
			data_mapped = []
			kingdoms = [item.text.lower() for item in termino_tree.xpath('/DATA/KINGDOM/ITEM/TERM') if item.text is not None] + [item.text.lower() for item in termino_tree.xpath('/DATA/KINGDOM/ITEM/SYNONYMS/SYN') if item.text is not None]
			species = [item.text.lower() for item in termino_tree.xpath('/DATA/SPECIE/ITEM/TERM') if item.text is not None]
			organisms = [item.text.lower() for item in termino_tree.xpath('/DATA/ORGANISM/ITEM/TERM') if item.text is not None]

			# PARSING
			for document in data:
				LINKS = {}
				for word in document['scored_words']:
					# STEP 1: KINGDOM
					if word[0] in kingdoms:
						if word[0] in [item.text.lower() for item in termino_tree.xpath('/DATA/KINGDOM/ITEM/TERM') if item.text is not None]:
							id_concept = termino_tree.xpath('/DATA/KINGDOM/ITEM[TERM="{}"]/ID'.format(word[0]))
						###########
						#~ ### WHAT ABOUT SYNONYMS? HOW TO CLIMB BACK ONE LEVEL TO GET ID FROM A IMBRICADED SYN?
						#~ elif word[0] in [item.text.lower() for item in termino_tree.xpath('/DATA/KINGDOM/ITEM/SYNONYMS/SYN') if item.text is not None]:
							#~ t = termino_tree.xpath('/DATA/KINGDOM/ITEM/SYNONYMS[SYN="{}"]'.format(word[0]))
							#~ print(word[0])
						##########
							try:
								if 'kingdoms' in LINKS.keys():
									LINKS['kingdoms'].append({id_concept[0].text: word})
								else:
									LINKS['kingdoms'] = [{id_concept[0].text: word}]
							except UnboundLocalError:
								pass
					# STEP 2: SPECIE
					if word[0] in species:
						id_concept = termino_tree.xpath('/DATA/SPECIE/ITEM[TERM="{}"]/ID'.format(word[0]))
						try:
							if 'species' in LINKS.keys():
								LINKS['species'].append({id_concept[0].text: word})
							else:
								LINKS['species'] = [{id_concept[0].text: word}]
						except UnboundLocalError:
							pass
					# STEP 3: ORGANISM
					if word[0] in organisms:
						id_concept = termino_tree.xpath('/DATA/ORGANISM/ITEM[TERM="{}"]/ID'.format(word[0]))
						try:
							if 'organisms' in LINKS.keys():
								LINKS['organisms'].append({id_concept[0].text: word})
							else:
								LINKS['organisms'] = [{id_concept[0].text: word}]
						except UnboundLocalError:
							pass


				document['links'] = LINKS
				data_mapped.append(document)

				if len(document['links'].keys()) > 0:
					print(document['file_name'])
					print(json.dumps(document['links'], indent=2, sort_keys=True, ensure_ascii=False))
					print(' ='*20)





if __name__ == '__main__':

	GDA = GenericDataAnalyzer(configuration='./configuration.cfg')
	if GDA.config.getboolean('options', 'train_model') is True:
		cleaned_data = GDA.data_preprocessing()
		scored_data = GDA.train_tfidf(data=cleaned_data)
	else:
		with open('tfidf_model.json', 'r') as model_saved:
			scored_data = json.loads(model_saved.read())
	GDA.analyze(data=scored_data)





