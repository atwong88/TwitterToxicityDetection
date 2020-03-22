import tweepy
import csv
import pandas as pd

from tweepy import OAuthHandler
consumer_key = '3T6YLgV51HOv8M1TaIoYTqNJ7'
consumer_secret = 'TDxBAHpwZ8rKVko6dT96RB8iak9aKgVDUoLfr02M3lWHZ6sL9K'
access_key = '188667470-hunlrSR3Dd4zpap331fT4a56w0TEl1JMMllFdpTT'
access_secret = 'YK44l9JNDAgZwyFZUiqYMlHD4ZpLX0v07EujRjx6XGsoa'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

KEYWORDS = ['fuck you','go die']
COLUMNNAMES = ['TweetID','ScreenName','TweetText','TweetDateTime','Followers']


Table = []
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):

        try:
            text = status.extended_tweet["full_text"]
        except:
            text = status.text
        
        if text[0:2] == 'RT':
            return
        
        name = status.user.screen_name
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at

        Row = []

        Row.append(id_str)
        Row.append(name)
        Row.append(text.encode("utf-8"))
        Row.append(created)
        Row.append(followers)
        
        Table.append(Row)
        print(Row)
        if len(Table) > 500:
            Saved = pd.DataFrame(Table,columns=COLUMNNAMES)
            Saved.to_csv('Saved.csv')

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener,tweet_mode='extended')
stream.filter(track=KEYWORDS)
