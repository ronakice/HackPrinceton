import tweepy
from textblob import TextBlob
import newssentiment
from newssentiment import SentimentVader
# Step 1 - Authenticate
consumer_key= 'O5FbmtO56q7mF7az8fEsjpKqg'
consumer_secret= 'X6Mfqjkoxi6iDNQq0NjIkFkr817yI8CApDHeChLExUxfWD6WXB'

access_token='127498866-CgXy6y20EIaKLWqQol8IXYL2zuVkAOPxXWdbB52g'
access_token_secret='7tYb02fePilYw98Y3PVOS1tlho5SpuVvImubHMF0jnD0Y'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 3 - Retrieve Tweets
public_tweets = api.search('Trump')
for tweet in public_tweets:
    print(tweet.text)

    #Step 4 Perform Sentiment Analysis on Tweets
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    d=SentimentVader(tweet.text)
    d.Senttext()
    X=[]
    for i in d.sslist:
        X.append(i['compound'])
    print(sum(X)/float(len(X)))
    #print(d.sslist)
    #print()
    print("")
