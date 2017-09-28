import tweepy, praw, markovify, re
from credentials import *
from credentialsreddit import *

#Twitter aggregation

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

twitter = tweepy.Cursor(api.search, q='bitcoin', lang='en').items(500)

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

reddit = praw.Reddit(client_id = r_client_id, client_secret = r_client_secret, password = r_password, user_agent = r_user_agent, username = r_username)

rfile = open('data/testreddit.txt', 'w')

for submission in reddit.subreddit('bitcoin').hot(limit=500):
    rfile.write(submission.title.encode('utf-8') + '\n')

rfile.close()

#Markov print

with open('data/test.txt') as ftwitter:
	texttwitter = ftwitter.read()

ftwitter.close()

with open('data/testreddit.txt') as freddit:
	textreddit = freddit.read()
	
freddit.close()

tmtwitter = markovify.NewlineText(texttwitter)

tmreddit = markovify.NewlineText(textreddit)

modelcombo = markovify.combine([ tmtwitter, tmreddit ])

regex_bitcoin = r'[^#](?i)(bitcoin)'

markov = modelcombo.make_short_sentence(140)
markov = re.sub(regex_bitcoin, ' #bitcoin', markov)
api.update_status(markov)
