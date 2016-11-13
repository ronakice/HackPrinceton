#!/usr/bin/env python
from tkinter import *
import json
import nltk
nltk.data.path.append("./nltk_data")
import urllib2
import newssentiment
from newssentiment import SentimentVader
import twitterminingandsent as tm
def Finale(keywords,fromDate,toDate):
	guardian_api = 'f82a10ba-1309-4ff7-ba94-9962249ea9e0'
	#keywords = ['clinton','trump','merkel','interest%20rates','iceland']
	#fromDate = '2016-09-01'
	#toDate = '2016-10-01'
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

teee,ss=Finale(l1,Starting,Ending)
print(teee)
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
plt.savefig('news.png')
plt.clf()
r=[]
x=[]
lab=[]
import matplotlib.pyplot as plt1
for i in teee:
	x.append(i["twitter"])
	r.append(i["occurances"]/1.0)
	lab.append(i["name"])
plt1.xlabel('Twitter Sentiment (-1  -  1)')

for i in range(0,len(x)):
	if x[i]<0.0:
		plt1.scatter(x[i],0 , r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)

	else:
		plt1.scatter(x[i],0, r[i]/1.0, c=random.rand(3,1),label=lab[i].replace("%20"," "),alpha=0.5)
plt1.legend(loc=2)
print("SECCC")
plt1.savefig('twitter.png')
##plt.show()
from PIL import Image
image=Image.open('news.png')
image2=Image.open('twitter.png')
image.show("NEWS")
image2.show("TWITTER")
