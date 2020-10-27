import json

import twitter

from keys import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=API_KEY,
                  consumer_secret=API_KEY_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

LAST_TWEET = None

last_tweet = open('last_tweet').read()
print('last tweet', last_tweet)

MAX_TWEETS = 10

start_tweeting = False
count_tweets = 0
for tweet in open("sortie.jsonl"):
	tweet = json.loads(tweet)
	if tweet.split('\n')[0].strip() == last_tweet.split('\n')[0].strip():
		start_tweeting = True
		continue
	if start_tweeting:
		print('tweeting', tweet)
		open('last_tweet', 'w').write(tweet)
		status = api.PostUpdate(tweet)
		count_tweets += 1
	if count_tweets == MAX_TWEETS:
		break