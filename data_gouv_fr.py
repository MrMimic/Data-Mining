import re
import time
import json
import urllib
import requests

''' Variables '''
start = time.time()
success = 0
error = 0
errorURL = []

''' Endpoint '''
url = 'https://www.data.gouv.fr/api/1/topics/'
response = urllib.request.urlopen(url)
data = response.read()
encoding = response.info().get_content_charset('utf-8')
dataGouv = json.loads(data.decode(encoding))
''' Parsing level 1 '''
for i in range(0, len(dataGouv['data'])):
	''' For every dataset '''
	for j in range(0, len(dataGouv['data'][i]['datasets'])):
		title = dataGouv['data'][i]['datasets'][j]['title']
		url = dataGouv['data'][i]['datasets'][j]['uri']
		''' Get second level '''
		try:
			response2 = urllib.request.urlopen(url)
			data2 = response2.read()
			encoding2 = response2.info().get_content_charset('utf-8')
			data2Gouv = json.loads(data2.decode(encoding))
		except:
			continue
		''' For every file '''
		for k in range(0, len(data2Gouv['resources'])):
			try:
				f = urllib.request.urlopen(data2Gouv['resources'][k]['url'])
				filename = dataGouv['data'][i]['name'] + '__' + title + '__' + data2Gouv['resources'][k]['title']
				urllib.request.urlretrieve(data2Gouv['resources'][k]['url'], filename) 
				print('Downloaded : {}'.format(f))
				success += 1
			except:
				errorURL.append(data2Gouv['resources'][k]['url'])
				error += 1
''' Get URL with no file downloaded '''
fToWrite = open('./0_ERROR_URL.csv', 'w')
for URL in errorURL:
	fToWrite.write(URL + '\n')
fToWrite.close()
print('Elapsed time : {}\nSuccess : {}\nError : {}'.format(time.time()-start, success, error))
