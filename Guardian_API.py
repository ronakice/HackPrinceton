#!/usr/bin/env python

import json
import nltk
nltk.data.path.append("./nltk_data")
import urllib2
import newssentiment
from newssentiment import SentimentVader
import twitterminingandsent as tm
def Finale():
	guardian_api = 'f82a10ba-1309-4ff7-ba94-9962249ea9e0'
	keywords = ['clinton','trump','merkel','interest%20rates','iceland']
	fromDate = '2016-09-01'
	toDate = '2016-10-01'
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
		json_obj = urllib2.urlopen(url)
		data = json.load(json_obj)
		items = data['response']
		Results = items['results']
		for ii in range(0, len(Results)):
			Titles = Results[ii]
			text= Titles['webTitle'].encode('utf-8','ignore')
			#print(text)
			d=SentimentVader(text)
			d.Senttext()
			L=[]
			for im in d.sslist:
				L.append(im['compound'])
			X[i].append((sum(L)/float(len(L))))
		t=0.0
		for ij in X[i]:
			t+=ij
				#t+=X[i][ik]
		t=t/float(len(X[i]))
		Sent[i]={"sentiment":{"news":t}}
	#print Sent
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
		json_obj = urllib2.urlopen(url)
		data = json.load(json_obj)
		items = data['response']
		Occurrances = items['total']
		Y[i].append(Occurrances)
	j=tm.printsent(keywords)
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
print(Finale())
teee,ss=Finale()
import matplotlib.pyplot as plt
r=[]
x=[]
lab=[]
print(ss)
for i in teee:
	x.append(i["news"])
	r.append(i["occurances"]/1.0)
	lab.append(i["name"])
with open('data21.txt', 'w') as outfile:
    json.dump(ss, outfile)
from numpy import random
plt.xlabel('News Sentiment (-1  -  1)')

for i in range(0,len(x)):
	if x[i]<0.0:
		plt.scatter(x[i],0 , r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)

	else:
		plt.scatter(x[i],0, r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)
plt.legend(loc=2)

print("GOO")
plt.show()
r=[]
x=[]
lab=[]
for i in teee:
	x.append(i["twitter"])
	r.append(i["occurances"]/1.0)
	lab.append(i["name"])
plt.xlabel('Twitter Sentiment (-1  -  1)')

for i in range(0,len(x)):
	if x[i]<0.0:
		plt.scatter(x[i],0 , r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)

	else:
		plt.scatter(x[i],0, r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)
plt.legend(loc=2)
plt.show()
#plt.show()
