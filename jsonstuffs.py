# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib2
import urllib
import sys
import base64
import json

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = 'd70e1ed408244e5787e051441715501a'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

input_texts = '{"documents":[{"id":"1","text":"hello world"},{"id":"2","text":"hello foo world"},{"id":"three","text":"hello my world"},]}'


# Detect sentiment.
batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
req = urllib2.Request(batch_sentiment_url, input_texts, headers)
req= urllib2.quote(req)

response = urllib2.urlopen(req)
result = response.read()
obj = json.loads(result)
for sentiment_analysis in obj['documents']:
    print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score']))
