from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity

from nltk.sentiment.vader import SentimentIntensityAnalyzer
text='''There has been a devastating earthquake in the Indian Ocean.
Tsunami hits Japan, thousands of people dead.
Britain decides to call it quit, leaves Europe causing nation to be in turmoil.
Donald Trump made President of the United States, country in danger.'''
from nltk import tokenize
lines_list = tokenize.sent_tokenize(text)
sid = SentimentIntensityAnalyzer()
for sentence in lines_list:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]))
    print("\n")
