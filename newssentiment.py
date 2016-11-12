from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

text= '''There has been a devastating earthquake in the Indian Ocean.
Tsunami hits Japan, thousands of people dead.
Britain decides to call it quit, leaves Europe causing nation to be in turmoil.
Donald Trump made President of the United States, country in danger.'''
d = SentimentVader(text)
d.Senttext()
#print(d.sslist)
