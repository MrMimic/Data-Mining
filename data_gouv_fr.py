import re
import time
import json
import requests
import urllib

start = time.time()

url = 'https://www.data.gouv.fr/api/1/topics/'
# https://www.data.gouv.fr/api/1/datasets/gares-ferroviaires-de-tous-types-exploitees-ou-non/
# Parsing lien en lien
# ttt fichier suivant type

response = urllib.request.urlopen(url)
data = response.read()
encoding = response.info().get_content_charset('utf-8')
dataGouv = json.loads(data.decode(encoding))


for i in range(0, len(dataGouv['data'])):
	
	for j in range(0, len(dataGouv['data'][i]['datasets'])):
		
		title = dataGouv['data'][i]['datasets'][j]['title']
		url = dataGouv['data'][i]['datasets'][j]['uri']
		
		try:
			response2 = urllib.request.urlopen(url)
			data2 = response2.read()
			encoding2 = response2.info().get_content_charset('utf-8')
			data2Gouv = json.loads(data2.decode(encoding))
		except:
			continue	
		
		
		print('- ' * 50)
		print('TOPIC : ' + dataGouv['data'][i]['name'])
		print('SOUS TOPIC ' + title)
		print(url)
		for k in range(0, len(data2Gouv['resources'])):
			print('DOCUMENT ' + data2Gouv['resources'][k]['title'])
			print('DOCUMENT ' + data2Gouv['resources'][k]['url'])
