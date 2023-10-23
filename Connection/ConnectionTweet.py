import tweepy
from decouple import config

def connect_twitter():
    try:
        consumer_key = config('consumer_key')
        consumer_secret = config('consumer_secret')
        access_token = config('access_token')
        access_token_secret = config('access_token_secret')

        # Autenticación en Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        return api
    except tweepy.TwitterServerError as error:
        return [{'message':error}]  # Maneja el error y retorna None o realiza otra acción en caso de error