
# sudo pip3 install TwitterSearch
# https://github.com/ckoepp/TwitterSearch
#https://api.twitter.com/1.1/search/tweets.json?q=startup+millions+investissement&result_type=mixed&count=100&lang=fr

from TwitterSearch import *

requested_terms = ['startup', 'millions', 'investissement']



''' Retrive Twitter '''
def get_news_on_twitter(requested_terms):
	try:
		tso = TwitterSearchOrder() # create a TwitterSearchOrder object
		
		tso.add_keyword(requested_terms) # let's define all words we would like to have a look for
		#tso.add_keyword(['startup millions']) # let's define all words we would like to have a look for
		tso.set_language('fr') # we want to see German tweets only
		tso.set_result_type('mixed') # we want to see German tweets only
		tso.set_count(100)
		#tso.set_include_entities(True) # and don't give us all those entity information
		#print(tso.create_search_url())
		
		# it's about time to create a TwitterSearch object with our secret tokens
		ts = TwitterSearch(
			consumer_key = '9EtnCfGKkd4sPdV1xnb9pbFrL',
			consumer_secret = 'aVoRtcCHiKRa9A03qQG5sBw0xcyaICD04cLp91VSBThprcL7SR',
			access_token = '163035097-6qc48iUfwjxB5I2gwR1ev7vEsKj9lmccppaBEYrH',
			access_token_secret = 'MQLdxQ4IkshMtnXE1bvD2jR1O73QRq4OkmeBhqjgBWEbX')
		
		# Dictionnary to handle tweets
		tweets = {}
		id_tweet = 1
		
		 # this is where the fun actually starts :)
		for tweet in ts.search_tweets_iterable(tso):
			hashList = []
			entities = []
			for hashtag in tweet['entities']['hashtags']:
				hashList.append(hashtag['text'])
			for entity in tweet['entities']['user_mentions']:
				entities.append(entity['name'])
				
			# Small dictionary used to add into the big one
			t = {}
			t['date'] = tweet['created_at']
			t['hashtags'] = ', '.join(hashList)
			t['text'] = tweet['text']
			t['entities'] = entities
			
			# FU-SION
			tweets[str(id_tweet)] = t
			id_tweet += 1
		
		return tweets
	
	except TwitterSearchException as e: # take care of all those ugly errors if there are some
		print(e)

 
 
if __name__ == '__main__':
	
	tweets = get_news_on_twitter(requested_terms)
	
	print(tweets)



