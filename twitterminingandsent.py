import tweepy
import nltk
nltk.data.path.append("./nltk_data")
from textblob import TextBlob
import newssentiment
from newssentiment import SentimentVader
import newssentiment
# Authenticate
consumer_key= 'O5FbmtO56q7mF7az8fEsjpKqg'
consumer_secret= 'X6Mfqjkoxi6iDNQq0NjIkFkr817yI8CApDHeChLExUxfWD6WXB'

access_token='127498866-CgXy6y20EIaKLWqQol8IXYL2zuVkAOPxXWdbB52g'
access_token_secret='7tYb02fePilYw98Y3PVOS1tlho5SpuVvImubHMF0jnD0Y'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
import urllib2
import urllib
import sys
import base64
import json
def printsent(keywords):
    # Azure portal URL.
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    # Your account key goes here.
    account_key = 'd70e1ed408244e5787e051441715501a'

    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

    #Retrieve Tweets

    twitt={}
    for j in keywords:
        input_texts = {"documents":[]}
        public_tweets = api.search(j)
        Z=[]
        ct=0
        for tweet in public_tweets:
            temp=[]
            ct+=1
            #print(tweet.text)
            z=tweet.text.encode('utf-8','ignore')


            input_texts["documents"].append({"id" :str(ct),"text":z})
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
        input_texts= json.dumps(input_texts)
        batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
        #print(batch_sentiment_url)
        #print(input_texts)
        req = urllib2.Request(batch_sentiment_url, input_texts, headers)
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        xe=[]
        for sentiment_analysis in obj['documents']:
            xe.append(sentiment_analysis['score']*2 - 1)
            #print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score']*2 - 1))
        #print(input_texts)
        #print(j)

        #print(Z)
        #print(sum(Z)/float(len(Z)))
        #print(sum(xe)/float(len(xe)))
        #print((2.0/3.0) * (sum(Z)/float(len(Z))) + (1.0/3.0)* (sum(xe)/float(len(xe))))
        twitt[j]=(2.0/3.0) * (sum(Z)/float(len(Z))) + (1.0/3.0)* (sum(xe)/float(len(xe)))
    return twitt
