import io
import sys
import os
import numpy as np
import pandas as pd
import nltk
import csv, collections
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from load_sentiment import load_sentiment
from gram_feature import gram_features
from extract_sentiment import sentiment_extract
from pos_feature import pos_features
from capital_feature import capitalization
import pickle


def get_features(sentence):
    print 'get features called ******************'
    features = {}
    gram_features(features,sentence)
    pos_features(features,sentence)
    sentiment_extract(features, sentence)
    capitalization(features,sentence)
    return features

def classify(sentence):
    #porter = nltk.PorterStemmer()
    #sentiments = load_sentiment()
    print 'classify.py classify method called ******************'
    features = get_features(sentence)
    val = [i for i in features.values()]
    loaded_model = pickle.load(open("model.pickle.dat", "rb"))
    y_pred = loaded_model.predict(val)
    return y_pred[0]












