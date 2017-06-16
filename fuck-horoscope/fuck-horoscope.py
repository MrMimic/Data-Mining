#!/usr/bin/python3

'''
The aim of this script is to fuck horoscope.
It download several horoscope in a famous french website.
Split data in sentences and count them.
Finally, plot a piegraph, showing sentences a used many times in horoscopes.
It prooves that shit is automatically generated. Thug life.
'''

import re
import json
import random
import socket
import urllib
import requests
from collections import Counter
import matplotlib.pyplot as plt

''' Parameters '''
parameters = {
	'i': 0,
	'p': 0,
	# Number of random horoscopes you want to download to make stats on
	'horoscopeNumber': 20000,
	# Print an array of sentence utilized more than 'sentenceUtilization' times
	'arrayCSV': True,
	# Number of times the sequence is used among every horoscopes to save it into the file
	'sentenceUtilization': 1,
	# Print a pieplot about sentence utilization is set on 'True'
	'piePlot': True,
	# Random dates to get horoscope or not (start from 01-01-1950) until it reach 'horoscopeNumber')
	'randomDate': False
}

''' Build session & co ''' 
post_URL = 'https://www.horoscope.fr/horoscope_custom/'
# Session
session = requests.Session()
# header
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})
tokenRequest = session.get(post_URL)
# Keep session Cookie
sessionCookies = tokenRequest.cookies
# Header
headers = {
    'Host': 'www.horoscope.fr',
	'Accept': '*/*',
	'Accept-Language': 'en,en-US;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'https://www.horoscope.fr/horoscope/perso',
	'Content-Length': '166',
	'DNT': '1',
	'Connection': 'keep-alive'
}

''' Get horoscope '''
def getHoroscope(year, month, day, date, horoscopeList, textList):
	# Data to send
	payload = {
		'birth_day':str(day),
		'birth_month':str(month),
		'birth_year':str(year),
		'birthdate':date,
		'birth_hour':'',
		'birth_min':'',
		'birthtime':'',
		'unknown_birthtime':'1',
		'birth_city_id':'2988507',
		'birth_city':'Paris+(France)'
	}
	# Encode it
	raw = urllib.parse.urlencode(payload)
	# POST requests
	r = session.post(post_URL, data=raw, cookies=sessionCookies, headers=headers)
	# Dictionary from results	
	dailyHoroscope = {}
	dailyHoroscope['BAD_GOOD'] = r.json()['response']['result'][0]['text']['bien']
	dailyHoroscope['BAD_BAD'] = r.json()['response']['result'][0]['text']['pasbien']
	dailyHoroscope['GOOD_GOOD'] = r.json()['response']['result'][1]['text']['bien']
	dailyHoroscope['GOOD_BAD'] = r.json()['response']['result'][1]['text']['pasbien']
	# Store every parts of the horoscope in a big list
	textList.append(dailyHoroscope['BAD_GOOD'])
	textList.append(dailyHoroscope['BAD_BAD'])
	textList.append(dailyHoroscope['GOOD_GOOD'])
	textList.append(dailyHoroscope['GOOD_BAD'])
	# Second dictionary with date as ID
	results = {}
	results[date] = dailyHoroscope
	horoscopeList.append(results)
	# Update the big list

''' Parse years '''
def parseYear(parsedYear):
	for year in range(1950, 2017):
			for month in range(1, 12):
				for day in range(1, 29):
					date = str(year) + '-' + str(month) + '-' + str(day)
					# If not in 'parsedYear' list
					if date not in parsedYear:
						parsedYear.append(date)
						return year, month, day, date
						
''' Execution '''
# Build a list of date to avoir redonduncy, a JSON list with date and a big oune containing all of the text.
passedDates = []
horoscopeList = []
textList = []
# Random date generation until it reachs parameters['horoscopeNumber']
if parameters['randomDate'] is True :
	while parameters['i'] < parameters['horoscopeNumber']:
		day = random.randint(1, 29)
		month = random.randint(1, 12)
		year = random.randint(1950, 2017)
		date = str(year) + '-' + str(month) + '-' + str(day)
		# If not into list
		if date not in passedDates:
			passedDates.append(date)
			try:
				getHoroscope(year, month, day, date, horoscopeList, textList)
			except:
				continue
		parameters['i'] += 1
		print('{} %\t{}'.format((parameters['i']*100)/parameters['horoscopeNumber'], date))
# From 1950/12/29 until it reachs parameters['horoscopeNumber']			
else:
	parsedYear = []
	while parameters['i'] < parameters['horoscopeNumber']:
		timeDate = parseYear(parsedYear)
		year = timeDate[0]
		month = timeDate[1]
		day = timeDate[2]
		date = timeDate[3]
		# If not into list
		if date not in passedDates:
			passedDates.append(date)
			try:
				getHoroscope(year, month, day, date, horoscopeList, textList)
			except:
				continue
		parameters['i'] += 1
		print('{} %\t\t\t{}'.format((parameters['i']*100)/parameters['horoscopeNumber'], date))
	
# End of requests Session
session.close()
# Let's join the list containing all of the text
joinedTextList = ''.join(textList)
splittedSentence = []
# And split it on the '.' to get list of sentences used.
for sentence in joinedTextList.split('. '):
	if sentence != '':
		splittedSentence.append(sentence)
# Count how many times a sentence have been used
counterDict =  Counter(splittedSentence)

''' Results CSV '''
if parameters['arrayCSV'] is True:
	horoscope = open('horoscope.csv', 'w')
	for sentence, count in counterDict.items():
		# Print if more than 1
		if count > parameters['sentenceUtilization']:
			horoscope.write(str(count) + '\t' + sentence + '\n')
	horoscope.close()

''' Results plot '''	
if parameters['piePlot'] is True:	
	counts = []
	# Count how many sentence have been used 1 time, 2 times, 3 times ...
	for count in counterDict.values():
		counts.append(count)
	counOfCounts = Counter(counts)
	# Extract label and counts to plot it
	labels = []
	sizes = []
	for label, count in counOfCounts.items():
		labels.append(label)
		sizes.append(count)
	# Plot results
	plt.pie(sizes, labels=labels, shadow=True, startangle=90, labeldistance=1.2)
	plt.axis('equal')
	plt.show()
