import tweepy

CONSUMER_KEY = 'W1YV441FkQls40s1VBZ3TvulQ'
CONSUMER_SECRET = 'zLz2VO9FGPjBv3BDy3z7KtXUx3gP2Y6OcxkSiw4mzZ2o7C3HJU'
ACCESS_TOKEN = '1467718945-DF2WgwNqbOvyvNN4Pbq2aRtomxy9xa6QjdWuoHo'
ACCESS_TOKEN_SECRET = 'mfqSz0tbizFqnExKf6WRWakKd0WRA3zQsTSTdEfZZ3PFF'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

status = "Test send from twitter app!"
api.update_status(status=status)