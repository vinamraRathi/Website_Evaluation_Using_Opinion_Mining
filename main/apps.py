from django.apps import AppConfig
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

class MainConfig(AppConfig):
    name = 'main'

    def textblob_score(sentence):
        return TextBlob(sentence, analyzer=NaiveBayesAnalyzer()).sentiment
    
    def textblob_score_PA(sentence):
        return TextBlob(sentence).sentiment.polarity