#!/usr/bin/python3

# # # #
# LARGE MAILING MINING
# # # #
# Search for queried terms into scientific APIs and extract emails
# Used for communication campaigns
# # # #
# 1.0		27/04/2017		Listing APIs
# 1.1		28/04/2017		Pubmed mining + extract position of the author in authors list
# 1.2		02/05/2017		Let make one functions for every journal to group set() and get()
# 1.3		10/05/2017		Springer extraction
''' IMPORTS '''
import json
import re
import urllib

import requests
from bs4 import BeautifulSoup
''' REGEXS '''
regexEmail = re.compile('[A-Za-z0-9._-]+@[A-Za-z0-9._-]{2,}\.[A-Za-z]{2,4}')
regexLastName = re.compile('<lastname>(.*)</lastname>')
regexArxivName = re.compile('From: (.*) \[<a href="https')
regexId = re.compile('</?id>')
regexFirstName = re.compile('<forename>(.*)</forename>')
regexPlosAuthorID = re.compile('<a class="author-name" data-author-id="([0-9]{1,2})">')
regexPlosName = re.compile('data-author-id="[0-9]{1,2}">(.*) <span class="')


class Requests:
    def __init__(self):
        ''' Nothing to initialize '''
        pass

    ###   PUBMED   ####					PMIDs > efetch > emails
    def getPubmedEmails(self, searchedTerm):
        ''' Search Pubmed with the searchedTerm to get a list of PMIDs in JSON format '''
        self.pubmedSearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=10000&format=json&term=' + searchedTerm
        pubmedRep = urllib.request.urlopen(self.pubmedSearch)
        pubmedData = pubmedRep.read()
        encoding = pubmedRep.info().get_content_charset('utf-8')
        pubmedJson = json.loads(pubmedData.decode(encoding))
        pmidsList = pubmedJson['esearchresult']['idlist']
        ''' Lists of emails on Pubmed '''
        pubmedEmails = []
        ''' For every PMID '''
        for pubmedID in pmidsList:
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
            authorsListPMID = efetchAuthors, pubmedID
            efetchAuthors = authorsListPMID[0]
            pubmedID = authorsListPMID[1]
            ''' Parse a list of authors in XML to extract names and affiliation (containing email) '''
            authorSoup = BeautifulSoup(str(efetchAuthors), 'html.parser')
            authorLastNameList = authorSoup.find_all('lastname')
            authorFirstNameList = authorSoup.find_all('forename')
            authorAffiliationList = authorSoup.find_all('affiliation')
            ''' If lists all have the same lenght '''
            if (len(authorLastNameList) == len(authorFirstNameList) == len(authorAffiliationList)):
                for a in range(0, len(authorAffiliationList) - 1):
                    if (re.findall(regexEmail, str(authorAffiliationList[a]))):
                        emailAdress = re.findall(regexEmail, str(authorAffiliationList[a]))[0]
                        ''' Main, last or other author ? '''
                        if (a == 0):
                            authorPosition = 'Main'
                        elif (a == (len(authorAffiliationList) - 1)):
                            authorPosition = 'Last'
                        else:
                            authorPosition = 'Other'
                        ''' Remove XML tag around names and return coordonates and source where email come from '''
                        authorLastName = re.findall(regexLastName, str(authorLastNameList[a]))[0]
                        authorFirstName = re.findall(regexFirstName, str(authorFirstNameList[a]))[0]
                        emailSource = 'Pubmed'
                        if (emailAdress not in pubmedEmails):
                            pubmedEmails.append(emailAdress)
                            print(authorPosition, authorLastName, authorFirstName, emailAdress, pubmedID, emailSource)

    ###   PLOS ONE   ###				PLOS id > wget URL > emails
    def getPlosEmails(self, searchedTerm):
        ''' Search PLOS with the searchedTerm to get a list of data in JSON format '''
        self.plosSearch = 'http://api.plos.org/search?wt=json&rows=10000&q=' + searchedTerm
        plosRep = urllib.request.urlopen(self.plosSearch)
        plosData = plosRep.read()
        encoding = plosRep.info().get_content_charset('utf-8')
        plosJson = json.loads(plosData.decode(encoding))
        plosIdList = plosJson['response']['docs']
        ''' Lists of emails on plOs '''
        plosEmails = []
        ''' For every plos ID '''
        for plosRawData in plosIdList:
            plosID = plosRawData['id']
            ''' Get list of authors for every plosID got from getPlosIds() '''
            plosURL = 'http://journals.plos.org/plospathogens/article?id=' + plosID
            ''' Simple URL scrapping, emails are stocked clearly in PLOS pages '''
            plosRep = requests.get(plosURL)
            plosData = plosRep.text
            plosSoup = BeautifulSoup(plosData, 'lxml')
            plosAuthors = plosSoup.find_all('li', attrs={'data-js-tooltip': 'tooltip_trigger'})
            ''' Parse a list of authors in XML to extract names and email '''
            plosAuthorSoup = BeautifulSoup(str(plosAuthors), 'lxml')
            plosAuthorsList = plosAuthorSoup.find_all('a', attrs={'class': 'author-name'})
            ''' Let's parse this list to search for 'email' tag '''
            for a in range(0, len(plosAuthorsList) - 1):
                if (re.search('email', str(plosAuthorsList[a]))):
                    ''' If yeah, get author ID '''
                    authorID = re.findall(regexPlosAuthorID, str(plosAuthorsList[a]))
                    authorEmailId = 'authCorresponding-' + authorID[0]
                    ''' And search for email adress with this ID '''
                    plosAuthorEmail = plosAuthorSoup.find_all('p', attrs={'id': authorEmailId})
                    if (plosAuthorEmail is not None):
                        ''' Main, last or other author ? '''
                        if (a == 0):
                            authorPosition = 'Main'
                        elif (a == (len(plosAuthorsList) - 1)):
                            authorPosition = 'Last'
                        else:
                            authorPosition = 'Other'
                        ''' Get clean name in all of XML tags '''
                        authorName = re.findall(
                            regexPlosName,
                            re.sub('\n', '', re.sub(' <span class="contribute"> </span>', '',
                                                    str(plosAuthorsList[a]))))[0]
                        ''' Get clean email '''
                        plosAuthorEmail = re.findall(regexEmail, str(plosAuthorEmail))[0]
                        emailSource = 'PLOS'
                        if (plosAuthorEmail not in plosEmails):
                            plosEmails.append(plosAuthorEmail)
                            print(authorPosition, authorName, plosAuthorEmail, plosID, emailSource)

    ###   ARXIV   ###					Page URL > Scrapping > names > esearch > emails
    def getArxivEmails(self, searchedTerm):
        ''' Search arXiv with the searchedTerm to get a list of publi title in XML '''
        self.arxiv = 'http://export.arxiv.org/api/query?max_results=10000&search_query=all:' + searchedTerm
        arxivRep = urllib.request.urlopen(self.arxiv)
        arxivData = arxivRep.read()
        arxivSoup = BeautifulSoup(arxivData, 'html.parser')
        urlList = arxivSoup.find_all('id')
        ''' Lists of emails on arXiv '''
        arxivEmails = []
        ''' For every title '''
        for idPageToGet in urlList:
            arxivURL = re.sub(regexId, '', str(idPageToGet))
            ''' Simple URL scrapping, last and first names are stocked clearly in arXiv pages '''
            arxivRep = requests.get(arxivURL)
            arxivData = arxivRep.text
            arxivSoup = BeautifulSoup(arxivData, 'lxml')
            try:
                contactName = re.findall(regexArxivName, str(arxivSoup))[0]
            except:
                continue
            ''' Now we get the contact name, search it on eSearch '''
            esearchContactNameURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=10000&format=json&term=' + contactName
            pubmedRep = urllib.request.urlopen(esearchContactNameURL)
            pubmedData = pubmedRep.read()
            encoding = pubmedRep.info().get_content_charset('utf-8')
            pubmedJson = json.loads(pubmedData.decode(encoding))
            pmidsList = pubmedJson['esearchresult']['idlist']
            ''' For every PMID '''
            for pubmedID in pmidsList:
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
                authorsListPMID = efetchAuthors, pubmedID
                efetchAuthors = authorsListPMID[0]
                pubmedID = authorsListPMID[1]
                ''' Parse a list of authors in XML to extract names and affiliation (containing email) '''
                authorSoup = BeautifulSoup(str(efetchAuthors), 'html.parser')
                authorLastNameList = authorSoup.find_all('lastname')
                authorFirstNameList = authorSoup.find_all('forename')
                authorAffiliationList = authorSoup.find_all('affiliation')
                ''' If lists all have the same lenght '''
                if (len(authorLastNameList) == len(authorFirstNameList) == len(authorAffiliationList)):
                    for a in range(0, len(authorAffiliationList) - 1):
                        if (re.findall(regexEmail, str(authorAffiliationList[a]))):
                            emailAdress = re.findall(regexEmail, str(authorAffiliationList[a]))[0]
                            ''' Main, last or other author ? '''
                            if (a == 0):
                                authorPosition = 'Main'
                            elif (a == (len(authorAffiliationList) - 1)):
                                authorPosition = 'Last'
                            else:
                                authorPosition = 'Other'
                            ''' Remove XML tag around names and return coordonates and source where email come from '''
                            authorLastName = re.findall(regexLastName, str(authorLastNameList[a]))[0]
                            authorFirstName = re.findall(regexFirstName, str(authorFirstNameList[a]))[0]
                            emailSource = 'arXiv'
                            if (emailAdress not in arxivEmails):
                                arxivEmails.append(emailAdress)
                                print(authorPosition, authorLastName, authorFirstName, emailAdress, arxivURL,
                                      emailSource)

    ###   SPRINGER   ###				DOI > Conversion > efetch > emails
    def getSpringerEmails(self, searchedTerm):
        ''' List to store every DOI, Springer's API send 50 resulsts / page max '''
        self.springerSearch = 'http://api.springer.com/metadata/json?api_key=<YOUR_API_KEY>=50&s=1&q=' + searchedTerm
        springerRep = urllib.request.urlopen(self.springerSearch)
        springerData = springerRep.read()
        encoding = springerRep.info().get_content_charset('utf-8')
        springerJson = json.loads(springerData.decode(encoding))
        ''' Get everything to parse results	'''
        start = int(springerJson['result'][0]['start'])
        total = int(springerJson['result'][0]['total'])
        pageLength = int(springerJson['result'][0]['pageLength'])
        springerDOI = []
        ''' Parse actual results page with one request / page to get DOI '''
        for pageCount in range(1, int((total / pageLength) + 2)):
            springerSearch = 'http://api.springer.com/metadata/json?api_key=<YOUR_API_KEY>=50&s=' + str(
                start) + '&q=' + searchedTerm
            springerRep = urllib.request.urlopen(springerSearch)
            springerData = springerRep.read()
            encoding = springerRep.info().get_content_charset('utf-8')
            springerJson = json.loads(springerData.decode(encoding))
            ''' Add DOIs to springerDOI list '''
            for result in springerJson['records']:
                if result['doi'] not in springerDOI:
                    springerDOI.append(result['doi'])
            start += 50
        springerEmails = []
        ''' Parse DOI list and convert it '''
        for uniqDOI in springerDOI:
            conversionRequest = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=' + uniqDOI + '&format=json&tool=test&email=<YOUR_EMAIL>'
            try:
                pubmedRep = urllib.request.urlopen(conversionRequest)
            except:
                continue
            pubmedData = pubmedRep.read()
            encoding = pubmedRep.info().get_content_charset('utf-8')
            pubmedJson = json.loads(pubmedData.decode(encoding))
            try:
                pubmedID = pubmedJson['records'][0]['pmid']
            except:
                continue
            ''' Get authors list in eFetch using PMIDs list returned by getPubmedPmids() '''
            efetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=' + pubmedID
            ''' Get PMID result as XML with eFetch '''
            efetchRep = urllib.request.urlopen(efetch)
            efetchData = efetchRep.read()
            encoding = efetchRep.info().get_content_charset('utf-8')
            efetchXml = efetchData.decode(encoding)
            ''' Parsing XML with BS4 to get authors lists '''
            efetchSoup = BeautifulSoup(efetchXml, 'html.parser')
            efetchAuthors = efetchSoup.find_all('author', attrs={'validyn': 'Y'})
            authorsListPMID = efetchAuthors, pubmedID
            efetchAuthors = authorsListPMID[0]
            pubmedID = authorsListPMID[1]
            ''' Parse a list of authors in XML to extract names and affiliation (containing email) '''
            authorSoup = BeautifulSoup(str(efetchAuthors), 'html.parser')
            authorLastNameList = authorSoup.find_all('lastname')
            authorFirstNameList = authorSoup.find_all('forename')
            authorAffiliationList = authorSoup.find_all('affiliation')
            ''' If lists all have the same lenght '''
            if (len(authorLastNameList) == len(authorFirstNameList) == len(authorAffiliationList)):
                for a in range(0, len(authorAffiliationList) - 1):
                    if (re.findall(regexEmail, str(authorAffiliationList[a]))):
                        emailAdress = re.findall(regexEmail, str(authorAffiliationList[a]))[0]
                        ''' Main, last or other author ? '''
                        if (a == 0):
                            authorPosition = 'Main'
                        elif (a == (len(authorAffiliationList) - 1)):
                            authorPosition = 'Last'
                        else:
                            authorPosition = 'Other'
                        ''' Remove XML tag around names and return coordonates and source where email come from '''
                        authorLastName = re.findall(regexLastName, str(authorLastNameList[a]))[0]
                        authorFirstName = re.findall(regexFirstName, str(authorFirstNameList[a]))[0]
                        emailSource = 'Springer'
                        if (emailAdress not in springerEmails):
                            springerEmails.append(emailAdress)
                            print(authorPosition, authorLastName, authorFirstName, emailAdress, uniqDOI, emailSource)

    ###   NATURE   ###					Names + titre > esearch > efetch > emails
    def getNatureEmails(self, searchedTerm):
        ''' blabla '''


''' This part can be parallelized (list of searchs with ID) '''
# Initialize our class
miner = Requests()
query = "Raman spectrometrie".replace(" ", "+")
# And get
miner.getPubmedEmails(query)
miner.getPlosEmails(query)
miner.getArxivEmails(query)
miner.getSpringerEmails(query)
