#!/usr/bin/env python3


import os
import re
import nltk
import math
import json
import string
import pandas as pd
import configparser
from lxml import etree
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob as tb
# sentiment analysis included
from matplotlib import pyplot as plt
from nltk.stem import WordNetLemmatizer

# Mapping termino AFTER tfIDF > acurracy increase

class GenericDataAnalyzer(object):

	def __init__(self, configuration):
		"""Generic textual data analyzer"""

		self.config = configparser.ConfigParser()
		self.config.read(configuration)
		# Get filelist
		self.base_directory = self.config.get('utilities', 'base_directory')
		self.file_list = os.listdir(self.base_directory)
		self.passed = 0
		# Dictionnary and punctuation
		self.stopwords = set(stopwords.words(self.config.get('utilities', 'corpus_lang')))
		self.punctuation = set(string.punctuation)
		# Pattern data
		with open(self.config.get('utilities', 'french_words'), 'r') as myfile:
			self.french_words = [word.strip('\n') for word in myfile if len(word) > 2]
		with open(self.config.get('utilities', 'french_departements'), 'r') as myfile:
			self.departements = [word.strip('\n').lower() for word in myfile]
		with open(self.config.get('utilities', 'french_regions'), 'r') as myfile:
			self.regions = [word.strip('\n').lower() for word in myfile]
		with open('./terminology/terminology_csv.csv', 'r') as my_terminology:
			termino_tree = pd.read_csv(my_terminology)
			self.kingdoms = [item.lower() for item in termino_tree['kingdom']]
			self.species = [item.lower() for item in termino_tree['group']]
			self.organisms = [item.lower() for item in termino_tree['organism']]

	def tf(self, word, blob):
		"""Term frequency"""
		return blob.words.count(word) / len(blob.words)

	def n_containing(self, word, bloblist):
		"""Number of occurence"""
		return sum(1 for blob in bloblist if word in blob.words)

	def idf(self, word, bloblist):
		"""Inverse document frequency"""
		return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

	def tfidf(self, word, blob, bloblist):
		"""TFIDF itself"""
		return self.tf(word, blob) * self.idf(word, bloblist)

	def find_ngrams(self, input_list, n):
		"""Gram a list"""
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
		"""TEXT PREPROCESSING"""

		cleaned_data = []
		lemmatiser = WordNetLemmatizer()
		print('\nTraining on {} documents.'.format(self.config['options']['number_of_documents']))
		for infile in self.file_list:
			if re.search('BSV', infile) and re.search('txt', infile):
				document_details = {}
				with open(self.base_directory+infile, 'r') as myfile:
					print('\t- Processing: {}...'.format(infile[:50]))
					# GET RAW DATA
					data = myfile.read().replace('\n', '').lower()
					document_details['raw'] = data
					# TOKENIZE AND GRAM
					#~ tokenized_data = nltk.word_tokenize(data)
					tokenized_data = re.findall(r"\w+(?:[-:]{1,2})?(?:\w+)?(?:[-:]{1,2})?(?:\w+)?", str(data))
					# CLEAN AND LEMME TOKENS
					lemmed_data = []
					for word in tokenized_data:
						if len(word) > 2:
							# IF WORD OK AND WELL SPELLED
							if (word not in self.stopwords) and (word not in self.punctuation):
								if word in self.french_words:
									lemmed_data.append(lemmatiser.lemmatize(word))
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
		"""Blabla"""

		# JOIN EVERY LEMMED TERMS IN A STR() FOR TEXTBLOB
		bloblist = []
		for extracted_document in data:
			bloblist.append(tb(' '.join(extracted_document['lemmed_data'])))
		# THEN, COMPUTE SCORES AND STOR THEM
		for indice in range(0, len(bloblist)):
			scores = {word: self.tfidf(word, bloblist[indice], bloblist) for word in bloblist[indice].words}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			data[indice]['scored_words'] = list(sorted_words)
		print('\n\nModel trained and words scored (TF-IDF).\n')
		# SAVE OR NOT
		if self.config.getboolean('options', 'save_model') is True:
			with open('tfidf_model.json', 'w') as model_file:
				model_file.write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

		return data

	def analyze(self, data):
		"""Blabla"""

		# ANALYZE (Steps have to be described in the config with CSV data)
		data_mapped = []
		words_found = []
		if self.config.getboolean('options', 'summarize_data') is True:
			for document in data:
				print('\n' + ' ='*20)
				print('\n{}\t({} words scorred)\n\n\tTop {} words:'.format(document['file_name'], len(document['scored_words']), self.config.getint('options', 'words_per_document')))
				LINKS = {}
				for word in document['scored_words'][:self.config.getint('options', 'words_per_document')]:
					print('\t\t- {}'.format(word))
					# Keep word for summary plot
					words_found.append(word[0])
					# TERMINOLOGY STEP 1: KINGDOM
					if word[0] in self.kingdoms:
						try:
							if 'kingdoms' in LINKS.keys():
								LINKS['kingdoms'].append(word)
							else:
								LINKS['kingdoms'] = [word]
						except (UnboundLocalError, IndexError):
							pass
					# TERMINOLOGY STEP 2: SPECIE
					if word[0] in self.species:
						try:
							if 'species' in LINKS.keys():
								LINKS['species'].append(word)
							else:
								LINKS['species'] = [word]
						except (UnboundLocalError, IndexError):
							pass
					# TERMINOLOGY STEP 3: ORGANISM
					for organism in self.organisms:
						if re.search(organism, word[0]):
							try:
								if 'organisms' in LINKS.keys():
									LINKS['organisms'].append(word)
								else:
									LINKS['organisms'] = [word]
							except (UnboundLocalError, IndexError):
								pass
					# GEOGRAPHY STEP1: REGIONS
					if word[0] in self.regions:
						try:
							if 'region' in LINKS.keys():
								LINKS['region'].append(word)
							else:
								LINKS['region'] = [word]
						except (UnboundLocalError, IndexError):
							pass
					# GEOGRAPHY STEP1: DEPARTEMENTS
					if word[0] in self.departements:
						try:
							if 'departements' in LINKS.keys():
								LINKS['departements'].append(word)
							else:
								LINKS['departements'] = [word]
						except (UnboundLocalError, IndexError):
							pass
				document['links'] = LINKS
				data_mapped.append(document)
				if len(document['links'].keys()) > 0:
					print('\n\tTerminology mapping:')
					print(json.dumps(document['links'], indent=2, sort_keys=True, ensure_ascii=False))

		# SUMMARY PLOT
		if self.config.getboolean('options', 'plot_graphes') is True:
			word_found_counted = Counter(words_found)
			score_min = self.config.getint('options', 'word_occurences_min')
			labels = [w[0] for w in word_found_counted.items() if w[1] > score_min]
			position = range(len(labels))
			counts = [w[1] for w in word_found_counted.items() if w[1] > score_min]

			figure = plt.figure()
			subplot = figure.add_subplot(111)
			subplot.bar(position, counts)
			subplot.set_xticks(range(len(labels)))
			subplot.set_xticklabels(labels, rotation=45)
			plt.show()


if __name__ == '__main__':

	GDA = GenericDataAnalyzer(configuration='./configuration.cfg')
	if GDA.config.getboolean('options', 'train_model') is True:
		cleaned_data = GDA.data_preprocessing()
		scored_data = GDA.train_tfidf(data=cleaned_data)
	else:
		with open('tfidf_model.json', 'r') as model_saved:
			scored_data = json.loads(model_saved.read())
	GDA.analyze(data=scored_data)
