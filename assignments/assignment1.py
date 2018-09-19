#!/usr/bin/python3

# Accessing the Twitter API
# This script describes the basic methodology for accessing a Twitter feed
# or something similar.

# Loading libraries needed for authentication and requests
import operator
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import json

# In order to use this script, you must:
# - Have a Twitter account and create an app
# - Store in keys.json a property called "twitter" whose value is an
#     object with two keys, "key" and "secret"
with open('keys.json', 'r') as f:
   keys = json.loads(f.read())['twitter']

twitter_key = keys['key']
twitter_secret = keys['secret']

# We authenticate ourselves with the above credentials
# We will demystify this process later
#
# For documentation, see http://requests-oauthlib.readthedocs.io/en/latest/api.html
# and http://docs.python-requests.org/en/master/
client = BackendApplicationClient(client_id=twitter_key)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://api.twitter.com/oauth2/token',
                          client_id=twitter_key,
                          client_secret=twitter_secret)

# Base url needed for all subsequent queries
base_url = 'https://api.twitter.com/1.1/'

# Particular page requested. The specific query string will be
# appended to that.
page = 'search/tweets.json'

# Depending on the query we are interested in, we append the necessary string
# As you read through the twitter API, you'll find more possibilities
req_url = base_url + page + '?q=Hanover+College&tweet_mode=extended&count=100'

# We perform a request. Contains standard HTTP information
response = oauth.get(req_url)

# Read the query results
results = json.loads(response.content.decode('utf-8'))

## Process the results
## CAUTION: The following code will attempt to read up to 10000 tweets that
## Mention Hanover College. You should NOT change this code.
tweets = results['statuses']
while True:
   if not ('next_results' in results['search_metadata']):
      break
   if len(tweets) > 10000:
      break
   next_search = base_url + page + results['search_metadata']['next_results'] + '&tweet_mode=extended'
   print(results['search_metadata']['next_results'])
   response = oauth.get(next_search)
   results = json.loads(response.content.decode('utf-8'))
   tweets.extend(results['statuses'])

## CAUTION: For the rest of this assignment, the list "tweets" contains all the
## tweets you would want to work with. Do NOT change the list or the value of "tweets".

# NUMBER 1
# List comprehension that prints out the full_text of our entire list of tweets.
texts = [tweet['full_text'] for tweet in tweets]
# print(texts)

# NUMBER 2
# Function that pulls full_text of a tweet based on if it's a retweet or not
def getFullText(tweet):
  if 'retweeted_status' in tweet:
    return tweet['retweeted_status']['full_text'];
  else:
    return tweet['full_text'];
fullTweets = [getFullText(tweet) for tweet in tweets]
# print(fullTweets)

# NUMBER 3
# This function gets the hashtag text from each tweet, if it has hashtags, and puts them into a list of strings
def getHashtagText(tweet):
  counter = len(tweet['entities']['hashtags'])
  hashtagList = []
  i = 0
  while counter > 0:
    hashtagList.append(tweet['entities']['hashtags'][i]['text'])
    counter = counter - 1
    i += 1
  return hashtagList
# This list comp pulls all of the hashtag texts from each tweet in tweets and makes list of hashtag texts for each
# tweet, then puts each of those lists into a larger list called tags_per_tweet
tags_per_tweet = [getHashtagText(tweet) for tweet in tweets]
# print(tags_per_tweet)

# NUMBER 4
# This problem go through tags_per_tweet and creates a dictionary that keeps track
# of how many times each hashtag was used like so... {hashtag: number of times used}
hashtags = {}
#hashtags[key] = "value"
for tweet in tags_per_tweet:
  for hashtag in tweet:
    if hashtag in hashtags:
      hashtags[hashtag] += 1
    else:
      hashtags[hashtag] = 1
# print(hashtags)

# NUMBER 5
# This problem prints out the 6 most used hashtags by sorting the hastags dictionary
# created in problem 4
sorted_hashtags = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)
top_six = []
for i in range(0,6):
  # print(sorted_hashtags[i])
  top_six.append(sorted_hashtags[i])
# print(top_six)

# NUMBER 6
# This problem creates a list of every tweet in tweets that has no hashtags
# This function returns a tweet only if it has no hashtag
def has_no_hashtag(tweet):
  if len(tweet['entities']['hashtags']) == 0:
    return tweet
hashtagless_tweets = [has_no_hashtag(tweet) for tweet in tweets]
# print(hashtagless_tweets)

# NUMBER 7
# {"hashtag": {"count": ..., "percent": ..., "users": ..., "other_tags": ...}}
tag_info = {}
for hashtag in hashtags:
  empty_dict = {}
  tag_info[hashtag] = empty_dict
  empty_dict['count'] = hashtags[hashtag]
  empty_dict['percentage'] = empty_dict['count'] / len(tweets)
  empty_dict['users'] = []
  for tweet in tweets:
    if hashtag in getHashtagText(tweet):
      if tweet['user']['screen_name'] not in empty_dict['users']:
        empty_dict['users'].append(tweet['user']['screen_name'])
  empty_dict['other_tags'] = []
  for tweet in tweets:
    if hashtag in getHashtagText(tweet):
      for tags in getHashtagText(tweet):
        if tags != hashtag:
          if tags not in empty_dict['other_tags']:
            empty_dict['other_tags'].append(tags)
  tag_info[hashtag] = empty_dict
# print(tag_info)

# NUMBER 8
# This code just takes our tag_info from problem 7 and writes
# the dictionary to a json file using "with open()" and "json.dump()"
with open('tag_info.json', 'w') as file:
  json.dump(tag_info, file)

# NUMBER 9
# This for loop builds our list of simpler tweets. Each entry being
# a dictionary containing info about each individual tweet from tweets
simpler_tweets = []
for tweet in tweets:
  tweet_entry = {}
  tweet_entry['text'] = tweet['full_text']
  tweet_entry['author'] = tweet['user']['screen_name']
  tweet_entry['date'] = tweet['created_at']
  tweet_entry['hashtags'] = getHashtagText(tweet)
  tweet_entry['mentions'] = [x['screen_name'] for x in tweet['entities']['user_mentions']]
  simpler_tweets.append(tweet_entry)

# Writes our simpler_tweets list to a json file.
with open('simpler_tweets.json', 'w') as file:
  json.dump(simpler_tweets, file)