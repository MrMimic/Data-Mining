
# sudo pip3 install TwitterSearch
# https://github.com/ckoepp/TwitterSearch
from TwitterSearch import *


try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    
    #tso.add_keyword(['startup', 'millions', 'investissement']) # let's define all words we would like to have a look for
    tso.add_keyword(['startup+millions+investissement&src=typd']) # let's define all words we would like to have a look for
    #tso.set_language('fr') # we want to see German tweets only
    #tso.set_result_type('mixed') # we want to see German tweets only
    #tso.set_count(100)
    #tso.set_include_entities(True) # and don't give us all those entity information

    print(tso.create_search_url())
	
    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'XXX',
        consumer_secret = 'XXX',
        access_token = 'XXX',
        access_token_secret = 'XXX'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print(tweet['text'])


except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)


# LESS RESULTAS THAN MANUAL SEARCH ? 
# APPLY SAME URL THAN SEARCH WINDOWS
