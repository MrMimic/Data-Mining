#!/usr/bin/python3

# # # # 
# OMICX PUBMED DATAMINING
# emeric.dynomant@omictools.com
# # # # 
# Script to mine Pubmed for new articles
# You give a key word (eg. RNA seq) and he'll find publication about RNA sequencing
# who contains an URL in the abstract (possible tool link) and who are NOT in omictools
# # # #
# v1.0:		03.04.2017		Request searched term and 'http OR https' in the abstract


print("Content-Type: text/html; charset=utf-8\n\n")
print()

import datetime										#
import re											#
import json											#
import requests 									#
import urllib.request								#
import ssl											#
import certifi										#
import cgi


form = cgi.FieldStorage()
print(form.getvalue('queryPM'))



toSearch = form.getvalue('queryPM')



# HEADER
print("Going to search Pubmed for: " + toSearch)
# OMICTOOLS API 64b CONNEXION
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(certifi.where())
httpsHandler = urllib.request.HTTPSHandler(context = context)
manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
manager.add_password(None, 'https://api.omictools.com/tools', 'cismef', '<APIKEY>')
authHandler = urllib.request.HTTPBasicAuthHandler(manager)
opener = urllib.request.build_opener(httpsHandler, authHandler)
urllib.request.install_opener(opener)
# GET DATA
response = urllib.request.urlopen('https://api.omictools.com/tools')
data = response.read()
# DECODE UTF-8
encoding = response.info().get_content_charset('utf-8')
omictools = json.loads(data.decode(encoding))
# MAKE A LIST OF PMIDS FROM OMICTOOLS
pmidListOmicx = []
for i in range(0,len(omictools)-1):
	if(omictools[i]["pmids"]):
		pmidListOmicx.append(omictools[i]["pmids"][0])
# BUILD PUBMED'S API REQUEST
req = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=xml&retmax=10000&term="+toSearch+"[Title/Abstract]+AND+(http[Title/Abstract]+OR+https[Title/Abstract])"
# GET PMIDs FROM PUBMED
response = urllib.request.urlopen(req)
pmidPubmed = response.read()
encoding = response.info().get_content_charset('utf-8')
pmidPubmedDecoded = pmidPubmed.decode(encoding)
# GET ONLY PMIDs IN RESPONSE
pmidList = re.findall('<Id>(.*)<\/Id>', pmidPubmedDecoded)
# COMPARISON WITH OUR DB
pmidNotInBase = []
for i in range(0, len(pmidList)-1):
	if(pmidList[i] not in pmidListOmicx):
		pmidNotInBase.append(pmidList[i])
# SUMMARY
print("PMID registered in Omictools' database: " + str(len(pmidListOmicx)))
print("PMID found with Pubmed's request: " + str(len(pmidList)))
print("PMID to classify: " + str(len(pmidNotInBase)))
# TITLE AND LINK PRINT
for i in range(0, len(pmidNotInBase)-1):

	pubReq = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=" + pmidNotInBase[i]
	pmidData = requests.get(pubReq)
	title = re.findall('<ArticleTitle>(.*)</ArticleTitle>', pmidData.text)

	print("##")
	print(title[0])
	print("https://www.ncbi.nlm.nih.gov/pubmed/" + pmidNotInBase[i])
	print("\n")



