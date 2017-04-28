#!/usr/bin/python3

# # # # 
# LARGE MAILING MINING
# emeric.dynomant@omictools.com
# # # # 
# Search for queried terms into scientific APIs and extract emails
# Used for communication campaigns 
# # # #

# # # #
# VERSIONNING
# # # #
# 1.0		27/04/2017		Listing APIs
# 1.1		28/04/2017		Pubmed mining + extract position of the author in authors list


''' IMPORTS '''
import re
import json
import urllib
import requests
from lxml import etree
from bs4 import BeautifulSoup

''' REGEXS '''
regexEmail = re.compile('[A-Za-z0-9._-]+@[A-Za-z0-9._-]{2,}\.[A-Za-z]{2,4}')
regexLastName = re.compile('<lastname>(.*)</lastname>')
regexFirstName = re.compile('<forename>(.*)</forename>')

class Requests:
	def __init__(self):
		
	###   PUBMED   ####					PMIDs > efetch > email
	def getPubmedPmids(self, searchedTerm):
		''' Search Pubmed with the searchedTerm to get a list of PMIDs in JSON format '''
		self.pubmedSearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=10000&format=json&term=' + searchedTerm
		pubmedRep = urllib.request.urlopen(self.pubmedSearch)
		pubmedData = pubmedRep.read()
		encoding = pubmedRep.info().get_content_charset('utf-8')
		pubmedJson = json.loads(pubmedData.decode(encoding))
		return pubmedJson['esearchresult']['idlist']
	
	def getPubmedAuthors(self, pubmedID):	
		''' Get authors list in eFetch using PMIDs list returned by getPubmedPmids() '''
		self._efetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=' + pubmedID
		''' Get PMID result as XML with eFetch '''
		efetchRep = urllib.request.urlopen(self._efetch)
		efetchData = efetchRep.read()
		encoding = efetchRep.info().get_content_charset('utf-8')
		efetchXml = efetchData.decode(encoding)
		''' Parsing XML with BS4 to get authors lists '''
		efetchSoup = BeautifulSoup(efetchXml, 'html.parser')
		efetchAuthors = efetchSoup.find_all('author', attrs={'validyn': 'Y'})
		return efetchAuthors, pubmedID
		
	def parsePubmedAuthors(self, efetchAuthors, pubmedID):
		''' Parse a list of authors in XML to extract names and affiliation (containing email) '''
		authorSoup = BeautifulSoup(str(efetchAuthors), 'html.parser')
		authorLastNameList = authorSoup.find_all('lastname')
		authorFirstNameList = authorSoup.find_all('forename')
		authorAffiliationList = authorSoup.find_all('affiliation')
		''' If lists all have the same lenght '''
		if(len(authorLastNameList) == len(authorFirstNameList) == len(authorAffiliationList)):
			for a in range(0, len(authorAffiliationList)-1):
				if(re.findall(regexEmail, str(authorAffiliationList[a]))):
					emailAdress = re.findall(regexEmail, str(authorAffiliationList[a]))[0]
					''' Main, last or other author ? '''
					if(a == 0):
						authorPosition = 'Main'
					elif(a == (len(authorAffiliationList)-1)):
						authorPosition = 'Last'
					else:
						authorPosition = 'Other'
					''' Remove XML tag around names '''
					authorLastName = re.findall(regexLastName, str(authorLastNameList[a]))[0]
					authorFirstName = re.findall(regexFirstName, str(authorFirstNameList[a]))[0]
					return authorPosition, authorLastName, authorFirstName, emailAdress, pubmedID
					
	
	###   PLOS ONE   ###						PLOS id > wget URL > email


hiCMining = Requests()
pmidsList = hiCMining.getPubmedPmids('Hi-C')
''' Get list of PMIDs about Hi-C '''
for pubmedID in pmidsList:
	''' Extract author list for every PMID returned '''
	authorsListPMID = hiCMining.getPubmedAuthors(pubmedID)
	''' Split authors list and PMID '''
	authorsList = authorsListPMID[0]
	actualPMID = authorsListPMID[1]
	''' Print coordonates if email is found in affiliations '''
	authorCoordonate = hiCMining.parsePubmedAuthors(authorsList, actualPMID)
	if(authorCoordonate is not None):
		print(authorCoordonate)


