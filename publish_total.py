import tweepy, markovify, re, random, schedule, time
from credentials import *
from credentialsreddit import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Markov print

with open("data/test.txt") as ftwitter:
	texttwitter = ftwitter.read()

ftwitter.close()

with open("data/testreddit.txt") as freddit:
	textreddit = freddit.read()
	
freddit.close()

tmtwitter = markovify.NewlineText(texttwitter)

tmreddit = markovify.NewlineText(textreddit)

modelcombo = markovify.combine([ tmtwitter, tmreddit ])

regex_bitcoin = r'[^#](?i)(bitcoin)'

def random_tweet():
	list = []

	for i in range(10):
		markov = modelcombo.make_short_sentence(140)
		markov = re.sub(regex_bitcoin, ' #bitcoin', markov)
		list.append(markov)

	lottery_winner = list[random.randrange(0, 10)]

	print lottery_winner
	api.update_status(lottery_winner)

random_tweet()

schedule.every(90).minutes.do(random_tweet)

while True:
    schedule.run_pending()
    time.sleep(1)
