#!/usr/bin/env python


# Importing the necessary libraries

from tkinter import Tk, Button, Label, Entry, Frame, TOP, RIGHT, LEFT, X, YES
from json import dumps
from json import loads
from nltk import data
from urllib2 import Request
from urllib2 import urlopen
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweepy import API
from tweepy import OAuthHandler
from textblob import TextBlob
from matplotlib.pyplot import xlabel
from matplotlib.pyplot import scatter
from matplotlib.pyplot import legend
from matplotlib.pyplot import savefig
from matplotlib.pyplot import clf
from matplotlib.pyplot import figure
from PIL import Image
from numpy import random
import sys
import base64



#---------------------------------------------------------------------------------------------------------------------------

data.path.append("./nltk_data")


# Vader machine learning news sentiment analysis

class SentimentVader:
    def __init__(self, text,sslist=[],lines_list=[]):
        self.sslist=[]
        self.text = text
        self.lines_list=[]

    def tokenizetext(self):
        self.lines_list = tokenize.sent_tokenize(self.text)

    def Senttext(self):
        self.tokenizetext()
        sid = SentimentIntensityAnalyzer()
        for sentence in self.lines_list:
            #print(sentence)
            m=sid.polarity_scores(sentence)
            self.sslist.append(sid.polarity_scores(sentence))
            t=len(self.sslist)
            for k in sorted(self.sslist[t-1]):
                pass
                #print('{0}: {1}, '.format(k, self.sslist[t-1][k]))
            #print("\n")
#			

#----------------------------------------------------------------------------------------------------------------------------



# Data mining functions



# Authenticate
consumer_key= 'O5FbmtO56q7mF7az8fEsjpKqg'
consumer_secret= 'X6Mfqjkoxi6iDNQq0NjIkFkr817yI8CApDHeChLExUxfWD6WXB'

access_token='127498866-CgXy6y20EIaKLWqQol8IXYL2zuVkAOPxXWdbB52g'
access_token_secret='7tYb02fePilYw98Y3PVOS1tlho5SpuVvImubHMF0jnD0Y'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = API(auth)


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
            z=tweet.text.encode('utf-8','ignore')


            input_texts["documents"].append({"id" :str(ct),"text":z})
            #Step 4 Perform Sentiment Analysis on Tweets
            analysis = TextBlob(tweet.text)
            temp.append(analysis.sentiment.polarity * analysis.sentiment.subjectivity)
            d=SentimentVader(tweet.text)
            d.Senttext()
            X=[]
            for i in d.sslist:
                X.append(i['compound'])
            temp.append(sum(X)/float(len(X)))
            Z.append(sum(temp)/float(len(temp)))
        input_texts= json.dumps(input_texts)
        batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
        req = Request(batch_sentiment_url, input_texts, headers)
        response = urlopen(req)
        result = response.read()
        obj = json.loads(result)
        xe=[]
        for sentiment_analysis in obj['documents']:
            xe.append(sentiment_analysis['score']*2 - 1)

        twitt[j]=(2.0/3.0) * (sum(Z)/float(len(Z))) + (1.0/3.0)* (sum(xe)/float(len(xe)))
    return twitt


	
def Finale(keywords,fromDate,toDate):
	guardian_api = 'f82a10ba-1309-4ff7-ba94-9962249ea9e0'
	X={}
	Sent={}
	for i in keywords:
		X[i] = []
		cut1 = 'http://content.guardianapis.com/search?from-date='
		cut2 = fromDate
		cut3 = '&to-date='
		cut4 = toDate
		cut5 = '&q='
		cut6 = i
		cut7 = '&api-key='
		cut8 = guardian_api
		urlSequence = [cut1,cut2,cut3,cut4,cut5,cut6,cut7,cut8]
		s = ''
		url = s.join(urlSequence)
		json_obj = urlopen(url)
		data = json.load(json_obj)
		items = data['response']
		Results = items['results']
		for ii in range(0, len(Results)):
			Titles = Results[ii]
			text= Titles['webTitle'].encode('utf-8','ignore')
			d=SentimentVader(text)
			d.Senttext()
			L=[]
			for im in d.sslist:
				L.append(im['compound'])
			X[i].append((sum(L)/float(len(L))))
		t=0.0
		for ij in X[i]:
			t+=ij
		t=t/float(len(X[i]))
		Sent[i]={"sentiment":{"news":t}}
	Y={}

	for i in keywords:
		Y[i] = []
		cut1 = 'http://content.guardianapis.com/search?from-date='
		cut2 = fromDate
		cut3 = '&to-date='
		cut4 = toDate
		cut5 = '&q='
		cut6 = i
		cut7 = '&api-key='
		cut8 = guardian_api
		urlSequence = [cut1,cut2,cut3,cut4,cut5,cut6,cut7,cut8]
		s = ''
		url = s.join(urlSequence)
		json_obj = urlopen(url)
		data = json.load(json_obj)
		items = data['response']
		Occurrances = items['total']
		Y[i].append(Occurrances)
	j=printsent(keywords)
	for i in Y.keys():
		Sent[i]["occurrances"]=Y[i][0]
		Sent[i]["sentiment"]["twitter"]=j[i]
	t1=[]
	ct=0
	for i in Y.keys():
		ct=ct+1
		l={}
		l["name"]=i
		l["occurances"]=Y[i][0]
		l["news"]=Sent[i]["sentiment"]["news"]
		l["twitter"]=Sent[i]["sentiment"]["twitter"]
		l=json.dumps(l)
		d = json.loads(l)
		t1.append(d)
	tempe= json.dumps(Sent)
	return t1,Sent


#------------------------------------------------------------------------------------------------------------------------------



# Setting up the graphical user interface (GUI).	
	
fields = 'Keyword 1', 'Keyword 2', 'Keyword 3', 'Keyword 4', 'Starting date [YYYY-MM-DD]','End date [YYYY-MM-DD]'
l1=[]
Starting=""
Ending=""

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      print(field[0])
      l1.append(text.replace(" ","%20"))
      print('%s: "%s"' % (field, text))

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=30, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

def GOOO():
	root = Tk()
	ents = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e)))
	b1 = Button(root, text='Show', command=(lambda e=ents: fetch(e)))
	b1.pack(side=LEFT, padx=5, pady=5)
	b2 = Button(root, text='Next', command=root.quit)
	b2.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()

GOOO()
Starting=l1[4]
Ending=l1[5]
l1=l1[:4]

KeywordArray,ss=Finale(l1,Starting,Ending)
print(KeywordArray)

#-----------------------------------------------------------------------------------------------------------------



#Plotting the results


r=[]
x=[]
lab=[]
print(ss)
for i in KeywordArray:
	x.append(i["news"])
	r.append(i["occurances"]/1.0)
	lab.append(i["name"])
with open('data21.txt', 'w') as outfile:
    json.dump(ss, outfile)

fig = figure()
ax1 = fig.add_subplot(111)
xlabel('News Sentiment (-1  -  1)')

for i in range(0,len(x)):
		ax1.scatter(x[i],0 , r[i]/1.0, c=random.rand(3,1), label=lab[i].replace("%20"," "), alpha=0.5)

lgnd = legend(loc=2)
lgnd.legendHandles[0]._sizes = [50]
lgnd.legendHandles[1]._sizes = [50]
lgnd.legendHandles[2]._sizes = [50]
lgnd.legendHandles[3]._sizes = [50]

savefig('news.png')
clf()


r=[]
x=[]
lab=[]

for i in KeywordArray:
	x.append(i["twitter"])
	r.append(i["occurances"]/1.0)
	lab.append(i["name"])

fig = figure()
ax1 = fig.add_subplot(111)
xlabel('Twitter Sentiment (-1  -  1)')

for i in range(0,len(x)):
		scatter(x[i],0 , r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)

legend(loc=2)
lgnd = legend(loc=2)
lgnd.legendHandles[0]._sizes = [50]
lgnd.legendHandles[1]._sizes = [50]
lgnd.legendHandles[2]._sizes = [50]
lgnd.legendHandles[3]._sizes = [50]


savefig('twitter.png')

image=Image.open('news.png')
image2=Image.open('twitter.png')
image.show("NEWS")
image2.show("TWITTER")
