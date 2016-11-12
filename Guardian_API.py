#!/usr/bin/env python

import json
import urllib2
import newssentiment
from newssentiment import SentimentVader
guardian_api = 'f82a10ba-1309-4ff7-ba94-9962249ea9e0'
keywords = ['clinton','trump','merkel','interest%20rates','iceland']

X={}

for i in keywords:
	X[i] = []
	cut1 = 'http://content.guardianapis.com/search?from-date=2016-06-01&q='
	cut2 = i
	cut3 = '&api-key=f82a10ba-1309-4ff7-ba94-9962249ea9e0'
	urlSequence = [cut1,cut2,cut3]
	s = ''
	url = s.join(urlSequence)
	json_obj = urllib2.urlopen(url)
	data = json.load(json_obj)
	items = data['response']
	Results = items['results']
	for ii in range(0, len(Results)):
		Titles = Results[ii]
		text= Titles['webTitle'].encode('utf-8','ignore')
		print(text)
		d=SentimentVader(text)
		d.Senttext()
		L=[]
		for im in d.sslist:
			L.append(im['compound'])
		X[i].append({text:(sum(L)/float(len(L)))})

print X
