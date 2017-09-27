import tweepy, praw
from credentials import *
from credentialsreddit import *

nbEntries = 0

class MyStreamListener(tweepy.StreamListener):
	def __init__(self):
		self.nbEntries = nbEntries
		super(tweepy.StreamListener, self).__init__()
	def on_status(self, status):
		print str(self.nbEntries) + 'TWITTER STREAM'
		print(status.text)
		self.nbEntries += 1
		if self.nbEntries >= 100:
			print 'CAP ATTEINT'
			return False
	def on_error(self, status_code):
		if status_code == 420:
			return False

print 'Authenticating on Twitter...'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

print 'Authenticating on Reddit...'

reddit = praw.Reddit(client_id = r_client_id, client_secret = r_client_secret, password = r_password, user_agent = r_user_agent, username = r_username)

print 'Launching Twitter Stream...'

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

myStream.filter(track = ['bitcoin'], async = True)

print 'Launching Reddit Stream...'

for submission in reddit.subreddit('bitcoin').stream.submissions():
    print str(nbEntries) + 'REDDIT STREAM'
    print(submission.title.encode('utf-8'))
    nbEntries += 1
    if nbEntries >= 150:
    	break
