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
		
		print(dataGouv['data'][i]['datasets'][j]['title'])
