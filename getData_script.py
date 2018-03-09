import json
import sys
from pymongo import MongoClient
import tweepy
from textblob import TextBlob

MONGO_HOST= 'mongodb://127.0.0.1:27017/twitterdb'  # assuming you have mongoDB installed locally
                                             # and a database called 'twitterdb'
query = sys.argv[1]
f_name = 'tweets_data4.json'
max_tweets=sys.argv[2]

CONSUMER_KEY = "yM0E6ME1FGrl7X9rMnarbYyzi"
CONSUMER_SECRET = "5WCL1APMB9btcOnRWGfb0sjuXlsINXiIVBUr9BnhsdD0FWSudi"
ACCESS_TOKEN = "2330590344-HDL1ZarQBBKuWy0KVuAS19GTUqIOq2tSdQBABJ5"
ACCESS_TOKEN_SECRET = "IwX4Zt1MSjQCmQ6TFQneJCN54C0Frs2wCm88oA76cUnWj"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

try:
    tweets = tweepy.Cursor(api.search,  q=query,
                             include_entities=True,
                             monitor_rate_limit=True, 
                             wait_on_rate_limit=True,
                             lang="en").items(max_tweets)
      
except tweepy.TweepError as e:
   raise e

client = MongoClient(MONGO_HOST)
count = 0
count_withOut = 0
for tweet in tweets:
    if tweet.coordinates is not None:
        count += 1
        data = json.dumps(tweet._json)
        new_data = json.loads(data)
        print (new_data['created_at'])
        text = new_data['text']
        coordinates = new_data['coordinates']['coordinates']
        created_at = new_data['created_at']
        print ("text: " + text)
        analisis = TextBlob(text)
        print (analisis.sentiment.polarity)
        polarity = analisis.sentiment.polarity
        
        if polarity > 0.3:
            res = "positive"
        elif polarity < 0:
            res = "negative"
        else: res = "neutral"
        key_state = query

        geo_json_feature = {
            "address": {
                "key_state": key_state,
                "coordinates": coordinates
            },
            "properties_text": {
                "text": text,
                "created_at": created_at,
                "sentiment": res,
                "polarity": polarity
            }
        }
        print(geo_json_feature)	
        
        db = client.twitterdb
        print("Connection Success!")
        db.twitter_data.insert(geo_json_feature)
        print("Data save Success")
        print ("Se han obtenido: ")
        print (count)
        print (" tweets para " + key_state)
    else: count_withOut += 1

print ("Se han obtenido: ")
print (count)
print (" tweets para " + key_state)
print (count_withOut)


	

