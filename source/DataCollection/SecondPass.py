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
api = tweepy.API(auth,wait_on_rate_limit=True)

COLUMNNAMES = ['ScreenName','Type','TweetID','TweetText','TweetDateTime'
              ,'Followers','Friends','Statuses','Favourites']

tweets_df = pd.read_csv('../data/sample.csv',header=None)
tweets_df.columns = ['Index','TweetID','UserName','TweetText','TweetDateTime','Followers','UserID']
tweets_df = tweets_df[['TweetID','UserName','TweetText','TweetDateTime','Followers','UserID']]
tweets_df['TweetID'] = tweets_df['TweetID'].astype(str)

tweetIDs = tweets_df['TweetID'].values

Table = []
Row = []
tweetsbuffer = []
for tweetid in tweetIDs:
    if len(tweetsbuffer) < 100:
        tweetsbuffer.append(tweetid)
    else:
        #get_tweet_list(api,tweetsbuffer)
        tweets = api.statuses_lookup(id_=tweetsbuffer, include_entities=False, trim_user=False)
        for tweet in tweets:
            Row.append(tweet.id_str)
            Row.append(tweet.created_at)
            Row.append(tweet.text.encode('UTF-8'))
            Row.append(tweet.user.screen_name)
            Row.append(tweet.user.followers_count)
            Row.append(tweet.user.friends_count)
            Row.append(tweet.user.statuses_count)
            Row.append(tweet.user.favourites_count)
            Table.append(Row)
            Row = []
        tweetsbuffer = []
if len(tweetsbuffer) > 0:
    tweets = api.statuses_lookup(id_=tweetsbuffer, include_entities=False, trim_user=False)
    for tweet in tweets:
        Row.append(tweet.id_str)
        Row.append(tweet.created_at)
        Row.append(tweet.text.encode('UTF-8'))
        Row.append(tweet.user.screen_name)
        Row.append(tweet.user.followers_count)
        Row.append(tweet.user.friends_count)
        Row.append(tweet.user.statuses_count)
        Row.append(tweet.user.favourites_count)
        Table.append(Row)
        Row = []

tweets_still_alive_df = pd.DataFrame(Table)
tweets_still_alive_df.columns = ['TweetID','TweetDateTime','TweetText','ScreenName','Followers','Following','TweetsCount','LikesCount']
tweets_still_alive_df['TweetID'] = tweets_still_alive_df['TweetID'].astype(str)

tweets_df_merged_still_alive_df = pd.merge(tweets_df,tweets_still_alive_df,how='left',on='TweetID')
tweets_df_merged_still_alive_df[tweets_df_merged_still_alive_df['TweetText_y'] != tweets_df_merged_still_alive_df['TweetText_y']]

def was_deleted(tweet_text):
    if tweet_text != tweet_text:
        return 1
    else:
        return 0

tweets_df_merged_still_alive_df['WasDeleted'] = tweets_df_merged_still_alive_df['TweetText_y'].apply(was_deleted)

tweets_new_df = tweets_df_merged_still_alive_df[['TweetID','UserName','TweetText_x','TweetDateTime_x','Followers_x','UserID','WasDeleted']]
tweets_new_df.columns = ['TweetID','UserName','TweetText','TweetDateTime','Followers','UserID','WasDeleted']

tweets_new_df.to_csv('../data/sample_with_label.csv')