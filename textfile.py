import tweepy
import praw
import markovify
import re
from credentials import *
from credentialsreddit import *

#Twitter aggregation

print 'Authenticating on Twitter...'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

print 'OK\nSearching...'

twitter = tweepy.Cursor(api.search, q='bitcoin', lang='en').items(500)

print 'OK\nFiltering tweets...'

tfile = open('data/test.txt', 'w')

regex_account = r'(@[\w]+(\:| |$))'
regex_mail = r'(http(.)+( |$))'

for tweet in twitter:
	if (not tweet.retweeted) and ('RT @' not in tweet.text):
		tweet.text[:tweet.text.find(':')]
		tweet.text = re.sub(regex_account, '', tweet.text)
		tweet.text = re.sub(regex_mail, '', tweet.text)
		tfile.write(tweet.text.encode('utf-8') + '\n')
		
tfile.close()

#Reddit aggregation

print 'OK\nAuthenticating on Reddit...'

reddit = praw.Reddit(client_id = r_client_id, client_secret = r_client_secret, password = r_password, user_agent = r_user_agent, username = r_username)

print 'OK\nSearching...'

rfile = open('data/testreddit.txt', 'w')

for submission in reddit.subreddit('bitcoin').hot(limit=500):
    rfile.write(submission.title.encode('utf-8') + '\n')

rfile.close()

#Markov print

print 'OK\nReading output files...'

with open("data/test.txt") as ftwitter:
	texttwitter = ftwitter.read()

ftwitter.close()

with open("data/testreddit.txt") as freddit:
	textreddit = freddit.read()
	
freddit.close()

print 'OK\nMarkovifying...'

tmtwitter = markovify.NewlineText(texttwitter)

tmreddit = markovify.NewlineText(textreddit)

modelcombo = markovify.combine([ tmtwitter, tmreddit ])

print 'OK\nDisplaying tweets...'

regex_bitcoin = r'[^#](?i)(bitcoin)'

for i in range(10):
	markov = modelcombo.make_short_sentence(140)
	markov = re.sub(regex_bitcoin, ' #bitcoin', markov)
	api.update_status(markov)
