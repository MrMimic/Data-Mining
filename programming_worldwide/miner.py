#!/usr/bin/python3



import time
import json
import requests


# Country list
countries = [country.strip('\n') for country in open('./countries_list.csv', 'r')]

# Get limit and wait if reached
request_limit = json.loads(requests.get('https://api.github.com/rate_limit').text)
if request_limit['rate']['remaining'] == 0:
	wait(10)

# Build results
results = {}
results['C'] = 0
results['Java'] = 0
results['JavaScript'] = 0
results['Perl'] = 0
results['PHP'] = 0
results['Python'] = 0
results['R'] = 0
results['Ruby'] = 0
results['Rust'] = 0

world_data = {}

# Parse countries
for country in countries:
	
	country_data = []
	
	
	for lang in [lang.strip('\n') for lang in open('prog_languages.txt', 'r')]:
		
		try:			
			# Get limit and wait if reached
			request_limit = json.loads(requests.get('https://api.github.com/rate_limit').text)
			if int(request_limit['resources']['search']['remaining']) == 0:
				to_sleep = int((int(request_limit['resources']['search']['reset']) - time.time()) + 1)
				print('Waiting {} sec ..'.format(to_sleep))
				time.sleep(to_sleep)
			
			# Then request
			req = 'https://api.github.com/search/users?q=location:' + country + '+language:' + lang
			data_country = json.loads(requests.get(req).text)
			
			results[lang] = results[lang] + int(data_country['total_count'])
			lang_data = {lang: data_country['total_count']}
			country_data.append(lang_data)
			
			print('{} devloppers in {} in {}'.format(data_country['total_count'], country, lang))
				

			
		except:
			print('Problem for {} in {}'.format(lang, country))
			continue
	
	
	world_data[country] = country_data
	
	
	print(results)

result_file = open('./RESULT_JSON.json', 'w')
result_file.write(world_data)
result_file.close()
