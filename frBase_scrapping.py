#!/usr/bin/python3


''' IMPORTS '''
import re
import json
import urllib
import string
import requests
from bs4 import BeautifulSoup as bs

''' REGEX '''
soupGetName = re.compile('title="(.*)">')
soupGetAdress = re.compile(' (.*)</a></div></div>')
soupGetFamilyName = re.compile('.html">(.*)</a>')
adressZip = re.compile('([0-9]{5})')
copainAvantURL = re.compile('<a href="(.*)"><figure style=')
copainAvantBDay = re.compile('">(.*)</abbr>')
copainAvantScolarity = re.compile(' {32}(.*)\t\t\t\t\t\t\t</a>')
copainAvantProfession = re.compile('<p class="title">(.*)</p>')
copainAVantPicture = re.compile('<meta content="(.*)" property="og:image"/>]')


class search:	
	''' Step 0: initiation '''
	def __init__(self):
		self.frBase = './frBase.json'
		
	
	''' Step 1: create a list of french family names '''
	def nameList(self):
		alphaList = list(string.ascii_lowercase)
		familyNamesList = []
		for letter in alphaList:
			# This website give the 230 most used family name per letter in France
			toScrap = 'http://www.nom-famille.com/commencant-par-' + letter + '/noms-les-plus-portes.html'
			repFamilyName = urllib.request.urlopen(toScrap)
			rawFamilyNameData = repFamilyName.read()
			fnSoup = bs(rawFamilyNameData, 'html.parser')
			familyNamesToAdd = fnSoup.find_all('a', attrs = {'class': 'nom'})
			# Add all of them in a list
			for rawFamily in familyNamesToAdd:
				familyName = re.findall(soupGetFamilyName, str(rawFamily))[0]
				familyNamesList.append(familyName)
		# Return a list of french family names
		print('Family names list loaded with {} names'.format(len(familyNamesList)))
		return familyNamesList
	
	
	''' Step 2: get name and actual adress from an official website '''		
	def adress(self, familyNamesList):
		frBaseList = []
		for keyName in familyNamesList:
			# Let's scrap french anuary
			toScrap = 'https://www.pagesjaunes.fr/pagesblanches/recherche?proximite=0&quoiqui=' + keyName
			PjRep = urllib.request.urlopen(toScrap)
			rawPjData = PjRep.read()
			PjSoup = bs(rawPjData, 'html.parser')
			rawPersons = PjSoup.find_all('header', attrs = {'class': 'v-card'})
			# Used to increment our contact ID
			ID = len(frBaseList)
			for contact in rawPersons:
				# People parsing
				contactSoup = bs(str(contact), 'html.parser')
				contactRawName = contactSoup.find_all('a', attrs = {'class': 'denomination-links pj-lb pj-link'})
				try:
					# Dictionary fill with contact informations
					personDict = {}
					personDict['id'] = ID
					personDict['name'] = re.findall(soupGetName, str(contactRawName))[0]
					personDict['fullAdress'] = re.findall(soupGetAdress, str(contact))[0]
					personDict['zip'] = re.findall(adressZip, str(contactAdress))[0]
				except:
					continue
				# Add person contact to our baselist
				frBaseList.append(personDict)
				ID += 1
		print('PagesJaunes scrapped for {} different profiles'.format(len(frBaseList)))
		return frBaseList
		
	
	''' Step 3: scrap social media to complete '''
	def social(self, frBaseList):
		frSOcialList = []
		# How many people are in CA
		count = 0
		# http://copainsdavant.linternaute.com
		for person in frBaseList:
			# Clean unsupported characters for URL construction
			nameCleaned = re.sub('[éèê]', 'e', person['name'])
			nameCleaned = re.sub('[ïî]', 'i', nameCleaned)
			toScrap = 'http://copainsdavant.linternaute.com/s?full&q=' + re.sub(' ', '+', nameCleaned) + '&ty=1'
			caRep = urllib.request.urlopen(toScrap)
			caRawData = caRep.read()
			caSoup = bs(caRawData, 'html.parser')
			rawPersonList = caSoup.find_all('div', attrs = {'class': 'grid_line gutter grid--norwd'})
			# Let's get person's profile URL to get ..
			for copain in rawPersonList:
				copainURL = 'http://copainsdavant.linternaute.com' + re.findall(copainAvantURL, str(copain))[0]
				copainPageRep = urllib.request.urlopen(copainURL)
				copainPageRaw = copainPageRep.read()
				copainSoup = bs(copainPageRaw, 'html.parser')
				# Birthday
				rawBirthDay = copainSoup.find_all('abbr', attrs = {'class': 'bday'})
				try:
					person['birthDay'] = re.findall(copainAvantBDay, str(rawBirthDay))[0]
					count += 1
				except:
					person['birthDay'] = 'N/A'
				# Actual profession
				rawProfession = copainSoup.find_all('p', attrs = {'class': 'title'})
				try:
					person['profession'] = re.findall(copainAvantProfession, str(rawProfession))[0]
				except:
					person['profession'] = 'N/A'
				# Scolarity places
				rawScolarity = copainSoup.find_all('a', attrs = {'class': 'jTinyProfileEtab notip jCareerLabel'})
				try:
					person['scolarity'] = re.findall(copainAvantScolarity, str(rawScolarity))
				except:
					person['scolarity'] = 'N/A'
				# A picture
				rawPictureURL = copainSoup.find_all('meta', attrs = {'property': 'og:image'})
				try:
					person['picture'] = re.findall(copainAVantPicture, str(rawPictureURL))[0]
				except:
					person['picture'] = 'N/A'
			# Add every profile to a list	
			frSOcialList.append(person)
		# Return that list
		print('CopainAvant extracted more information for {} of the {} persons in total'.format(count, len(frSOcialList)))
		return frSOcialList
		
		
	''' Last step : print result in a json file '''	
	def outPrint(self, toPrint):	
		jsonEncoded = json.dumps(toPrint, indent=4)
		frBaseFile = open(self.frBase, 'w')
		frBaseFile.write(jsonEncoded)
		frBaseFile.close()	
		

			
''' EXECUTION '''
search = search()
familyNamesList = search.nameList()
#familyNamesList = ['Yalap', 'Ysebaert']
frBaseList = search.adress(familyNamesList)
frSOcialList = search.social(frBaseList)
search.outPrint(frSOcialList)
