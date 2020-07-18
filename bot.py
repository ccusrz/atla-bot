import tweepy
import random
import time
import logging
from constants import transcripts
from os import environ

#Declaring credentials
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

#Every hour a new tweet will be posted
INTERVAL = 60 * 60 

def friendships(api):
	
	followers = api.followers_ids('avatar_texts')
	friends = api.friends_ids('avatar_texts')

	#Following non-protected followers
	for user in followers:
		try:
			if user not in friends and not api.get_user(user).protected:
				api.get_user(user).follow()
		except tweepy.TweepError:
			continue

	#Unfollowing non-followers
	for user in friends:
		try:
			if user not in followers:
				api.destroy_friendship(user)
		except tweepy.TweepError:
			continue

def poster(api):

	try:
		api.update_status(random.choice(transcripts))
	except tweepy.TweepError as err:
		if err.api_code == 187:
			logging.error("Status duplicated")
		else:
			raise err

def main():

	logging.basicConfig(level=logging.INFO)

	#Logging in credentials to Twitter API
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

	#Authenticating while setting up boundaries
	api = tweepy.API(auth, wait_on_rate_limit = True,
		wait_on_rate_limit_notify = True)

	#Validating credentials
	try:
		api.verify_credentials()
		logging.info('Authentication OK')
	except:
		logging.error("Error during Authentication")
	
	#Running bot
	while True:
		poster(api)
		friendships(api)
		time.sleep(INTERVAL)

if __name__ == '__main__':
	main()
