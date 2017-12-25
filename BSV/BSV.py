#!/usr/bin/env python3



import os
import re
import nltk
import math
import json
import string
from collections import Counter
from nltk.corpus import stopwords

from textblob import TextBlob as tb




class AnalyzeBSV(object):


	def __init__(self):
		
		self.base_directory = '/home/emeric/1_Github/Data-Mining/data_gouv_utilisation/projets/musk/pestobserver/reportsOCR/' 
		self.file_list = os.listdir(self.base_directory)

		self.passed = 0
		self.number_of_documents = 100
		self.words_per_document = 10

		self.stopwords = set(stopwords.words('french'))
		self.punctuation = set(string.punctuation)
		with open('./liste_mots_francais.txt', 'r') as myfile:
			self.french_words = [word.strip('\n') for word in myfile]
		# GEGRAPHY
		with open('./departements.txt', 'r') as myfile:
			self.departements = [word.strip('\n').lower() for word in myfile]
		with open('./regions.txt', 'r') as myfile:
			self.regions = [word.strip('\n').lower() for word in myfile]
		# CULTURE
		self.vegetables = ['salade', 'tomate', 'oignion', 'chou', 'carotte', 'brocolis', 'betterave', 'haricots', 'asperges', 'pois', 'tabac']
		self.fruits = ['fraise', 'poire', 'pomme', 'pruneau', 'coing', 'brugnon', 'pêche', 'mirabelle', 'citrons', 'oranges', 'kiwi', 'cerise', 'banane', 'melon']
		self.cereals = ['riz', 'épeautre', 'avoine', 'blé', 'maïs', 'colza', 'seigle', 'orge']
		# RAVAGEURS
		self.virus = ['jaunisse', 'mosaïque', 'nanisme', 'striure']
		self.bacteries = ['pseudomonas', 'xanthomonas', 'clavibacter']
		self.ravageurs = ['doryphores', 'charançon', 'cochenille', 'criquets', 'termites']
		self.champignons = ['piétin', 'mildiou', 'galle', 'chancre', 'ergot', 'septriose', 'rouille', 'fusarium', 'aspergillus', 'penicillium']




	def tf(self, word, blob):
		return blob.words.count(word) / len(blob.words)


	def n_containing(self, word, bloblist):
		return sum(1 for blob in bloblist if word in blob.words)


	def idf(self, word, bloblist):
		return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))


	def tfidf(self, word, blob, bloblist):
		return self.tf(word, blob) * self.idf(word, bloblist)


	def stat(self):

		# TRANING
		bloblist = []
		print('\nTraining on {} documents.\n'.format(self.number_of_documents))
		for infile in self.file_list:
			if re.search('BSV', infile) and re.search('txt', infile):
				with open(self.base_directory+infile, 'r') as myfile:
					data = myfile.read().replace('\n', '').lower()
					blob_data = nltk.word_tokenize(data)
					bloblist.append(tb(data))
					self.passed += 1
				if self.passed == self.number_of_documents:
					break

		# PARSING
		for i, blob in enumerate(bloblist):
			# EMPTY STORAGE
			DOCUMENT = {}
			VEGETABLES = []
			FRUITS = []
			CEREALS = []
			REGIONS = []
			DEPARTEMENT = []
			VIRUS = []
			BACTERIES = []
			RAVAGEURS = []
			CHAMPIGNONS = []
			# TF_IDF
			scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
			sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
			scored_words = []
			printed = 0
			for word, score in sorted_words:
				# CULTURE
				if word in self.vegetables and word not in VEGETABLES:
						VEGETABLES.append('{} ({})'.format(word, round(score, 5)))
				if word in self.fruits and word not in FRUITS:
						FRUITS.append('{} ({})'.format(word, round(score, 5)))
				if word in self.cereals and word not in CEREALS:
						CEREALS.append('{} ({})'.format(word, round(score, 5)))
				# RAVAGEURS
				if word in self.virus and word not in VIRUS:
					VIRUS.append('{} ({})'.format(word, round(score, 5)))
				if word in self.bacteries and word not in BACTERIES:
					BACTERIES.append('{} ({})'.format(word, round(score, 5)))
				if word in self.ravageurs and word not in RAVAGEURS:
					RAVAGEURS.append('{} ({})'.format(word, round(score, 5)))
				if word in self.champignons and word not in CHAMPIGNONS:
					CHAMPIGNONS.append('{} ({})'.format(word, round(score, 5)))
				# GEOGRAPHIC
				if word in self.departements and word not in DEPARTEMENT:
						DEPARTEMENT.append('{} ({})'.format(word, round(score, 5)))
				if word in self.regions and word not in REGIONS:
						REGIONS.append('{} ({})'.format(word, round(score, 5)))
				# TOP SCORE
				if (len(word) > 2) and (word not in self.stopwords) and (word not in self.punctuation) and (word in self.french_words):
					if printed < self.words_per_document:
						scored_words.append('{} ({})'.format(word, round(score, 5)))
						printed += 1




			# TOP SCORE
			DOCUMENT['top_mots'] = scored_words
			# DATE
			if re.search('[0-9]{2}/[0-9]{2}/20[0-9]{2}', str(blob)): DOCUMENT['date'] = (re.findall('[0-9]{2}/[0-9]{2}/20[0-9]{2}', str(blob)))
			else: DOCUMENT['date'] = list(set((re.findall('20[0-9]{2}', str(blob)))))
			# CULTURE
			CULTURES = {}
			if len(VEGETABLES) > 0: CULTURES['legumes'] = VEGETABLES
			if len(FRUITS) > 0: CULTURES['fruits'] = FRUITS
			if len(CEREALS) > 0: CULTURES['cereales'] = CEREALS
			if len(CULTURES.keys()) > 0: DOCUMENT['cultures'] = CULTURES
			# RAVAGEURS
			DANGERS = {}
			if len(VIRUS) > 0: DANGERS['virus'] = VIRUS
			if len(BACTERIES) > 0: DANGERS['bacteries'] = BACTERIES
			if len(RAVAGEURS) > 0: DANGERS['ravageurs'] = RAVAGEURS
			if len(CHAMPIGNONS) > 0: DANGERS['champignons'] = CHAMPIGNONS
			if len(DANGERS.keys()) > 0: DOCUMENT['dangers'] = DANGERS
			# GEOGRAPHICS
			GEOGRAPHY = {}
			if len(DEPARTEMENT) > 0: GEOGRAPHY['departement'] = DEPARTEMENT
			if len(REGIONS) > 0: GEOGRAPHY['regions'] = REGIONS
			if len(GEOGRAPHY.keys()) > 0: DOCUMENT['geographie'] = GEOGRAPHY


			print('{} Document {} {}'.format('='*20, i+1, '='*20))
			print(json.dumps(DOCUMENT, indent=2, ensure_ascii=False, sort_keys=True))

