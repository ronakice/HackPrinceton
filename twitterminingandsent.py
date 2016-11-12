import tweepy
from textblob import TextBlob
import newssentiment
from newssentiment import SentimentVader
# Authenticate
consumer_key= 'O5FbmtO56q7mF7az8fEsjpKqg'
consumer_secret= 'X6Mfqjkoxi6iDNQq0NjIkFkr817yI8CApDHeChLExUxfWD6WXB'

access_token='127498866-CgXy6y20EIaKLWqQol8IXYL2zuVkAOPxXWdbB52g'
access_token_secret='7tYb02fePilYw98Y3PVOS1tlho5SpuVvImubHMF0jnD0Y'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Retrieve Tweets
keywords=['Trump', 'Hillary', 'brexit', 'America']
for j in keywords:
    public_tweets = api.search(j)
    Z=[]
    for tweet in public_tweets:
        temp=[]
        #print(tweet.text)

        #Step 4 Perform Sentiment Analysis on Tweets
        analysis = TextBlob(tweet.text)
        temp.append(analysis.sentiment.polarity * analysis.sentiment.subjectivity)
        #print(analysis.sentiment.polarity * analysis.sentiment.subjectivity)
        d=SentimentVader(tweet.text)
        d.Senttext()
        X=[]
        for i in d.sslist:
            X.append(i['compound'])
        temp.append(sum(X)/float(len(X)))
        #print(temp[1])
        #print("AVG POLARITY: ")
        Z.append(sum(temp)/float(len(temp)))
        #print(sum(temp)/float(len(temp)))
        #print(d.sslist)
        #print()
        #print("")
    print(j)
    print(Z)
    print(sum(Z)/float(len(Z)))
