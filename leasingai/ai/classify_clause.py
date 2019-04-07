from __future__ import division
import io
import sys
import os
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import csv, collections
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from .load_sentiment import load_sentiment
from .gram_feature import gram_features
from .extract_sentiment import sentiment_extract
from .pos_feature import pos_features
from .capital_feature import capitalization
#from load_sentiment import load_sentiment
#import cPickle
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import math
import pdb


def gram_features(features, sentence):
    porter = nltk.PorterStemmer()
    if sentence:
      sentence_rep = sentence
    else:
      sentence_rep = ''
    token = nltk.word_tokenize(sentence_rep)
    #print(token,"------------token--------------")
    token = [porter.stem(i.lower()) for i in token]  
    bigrams = nltk.bigrams(token) 
    
    bigrams = [tup[0] + ' ' + tup[1] for tup in bigrams]
    print (bigrams)
    grams = token + bigrams
    #print(grams,"-------------bigrams-------------")
    return grams


def pos_vector(sentence):
    pos_tag = nltk.pos_tag(sentence)
    #print(pos_tag)
    vector = np.zeros(4)
        
    for i in range(0, len(pos_tag)):
       
        pos = pos_tag[i][1]
        #print(pos)
        if pos[0:2]=='NN':
            vector[0] += 1
        elif pos[0:2] =='JJ':
            vector[1] += 1
        elif pos[0:2] =='VB':
            vector[2] += 1
        elif pos[0:2] == 'RB':
            vector[3] += 1
                
    return vector


def pos_features(features,sentence):
    porter = nltk.PorterStemmer()
    #sentiments = load_sentiment()
    sentence_rep = sentence
    token = nltk.word_tokenize(sentence_rep)
    token = [ porter.stem(each.lower()) for each in token]
    
    pos_vector1 = pos_vector(token)
    
    for j in range(len(pos_vector1)):
        features['POS_'+str(j+1)] = pos_vector1[j]
    

def get_features(sentence):
    features = {}
    gram_features(features,sentence)
    pos_features(features,sentence)
    
    sentiment_extract(features, sentence)
    capitalization(features,sentence)
    return features



def matching_rate(sentence, key_text):
    features = {}
    feature1 = gram_features(features, sentence)
    feature2 = gram_features(features, key_text)
    length2 = len(feature2)
    count_matching = 0
    for gram in feature2:
        if(gram in feature1):
            count_matching = count_matching + 1
            
    rate = 0.1
    if(length2== 0):
        length2 = 1
    rate = count_matching / length2
 
    if(rate > 0.75):return 1
    else: return 0
def type_sentence(sentence):
    token = nltk.word_tokenize(sentence)
    porter = nltk.PorterStemmer()
    token = [porter.stem(i.lower()) for i in token]
    pos_token = nltk.pos_tag(token)
    
    sub_conjuntions = []
    sub_conjuntions.append("after")
    sub_conjuntions.append("although")
    sub_conjuntions.append("as")
    sub_conjuntions.append("because")
    sub_conjuntions.append("before")
    sub_conjuntions.append("even if")
    sub_conjuntions.append("even though")
    sub_conjuntions.append("if")
    sub_conjuntions.append("since")
    sub_conjuntions.append("so that")
    sub_conjuntions.append("than")
    sub_conjuntions.append("that")
    sub_conjuntions.append("though")
    sub_conjuntions.append("unless")
    sub_conjuntions.append("until")
    sub_conjuntions.append("when")
    sub_conjuntions.append("whenever")
    sub_conjuntions.append("where")
    sub_conjuntions.append("whereas")
    sub_conjuntions.append("wherever")
    sub_conjuntions.append("whether")
    sub_conjuntions.append("while")
    sub_conjuntions.append("why")

    coor_conjuntions = []
    coor_conjuntions.append("for")
    coor_conjuntions.append("and")
    coor_conjuntions.append("nor")
    coor_conjuntions.append("but")
    coor_conjuntions.append("or")
    coor_conjuntions.append("yet")
    coor_conjuntions.append("so")

    type_sentence = "simple"
    counter_clause = 0
    for pos_Etoken in pos_token:
        if pos_Etoken[1] == "IN":
            if pos_Etoken[0] in sub_conjuntions:
                type_sentence = "complex"
            
        if pos_Etoken[1] == "CC":
            if pos_Etoken[0] in coor_conjuntions:
                if type_sentence == "complex":
                    type_sentence == "complex"
                else:
                    type_sentence = "compound"
        if pos_Etoken[1] == ",":
            counter_clause = 1
    if counter_clause == 0:
        type_sentence = "simple"
    return type_sentence

def type_percentage(text):
    count_simple = 0
    count_complex = 0
    count_compound = 0
    sent_tokenize_list = sent_tokenize(text)
    for sentence in sent_tokenize_list:
        if type_sentence(sentence) == "simple":
            count_simple = count_simple + 1
        if type_sentence(sentence) == "complex":
            count_complex = count_complex + 1
        if type_sentence(sentence) == "compound":
            count_compound = count_compound + 1
    count = count_simple + count_complex + count_compound
    count_simple = (count_simple/count) * 100
    count_complex = (count_complex/count) * 100
    count_compound = (count_compound/count) * 100
    #rint("%s simple %s complex %s compound sentence"%(count_simple, count_complex, count_compound))

def number_different_words(text):
    token = nltk.word_tokenize(text)
    porter = nltk.PorterStemmer()
    token = [porter.stem(i.lower()) for i in token]
    token_count = 0
    for each_token in token:
        token_count = token_count + 1

    count = Counter(token)
    total_number = 0
    for each_count in count:
        check_word = each_count[0]
        if check_word.isalpha():
            total_number = total_number + 1
    #print(total_number)
    #print(token_count)

def relatedness_words(text):
    token = nltk.word_tokenize(text)
    porter = nltk.PorterStemmer()
    token = [porter.stem(i.lower()) for i in token]
    count = Counter(token)
    highest = 0
    for each_count in count:
        if highest < count[each_count]:
            highest = count[each_count]
    
    for each_count in count:
        count[each_count] = math.floor(count[each_count] * 9 / highest) + 1
    #print(count)

def number_complexwords(text):
    text = text.lower()
    token = nltk.word_tokenize(text)
    stemmer = SnowballStemmer("english")
    count = 0
    for each_token in token:
        stem_word = stemmer.stem(each_token)
        if stem_word != each_token:
            count = count + 1
    #print(count)
    return count   
    #print(stemmer.stem("generalized"))
    #print(stemmer.stem("generalization"))
    #print(stemmer.stem("unhappy"))
    
    #WNL = WordNetLemmatizer()
    #print(WNL.lemmatize('ladies'))
    #print(WNL.lemmatize('saying'))
# -*- coding: utf-8 -*-
text = "Too much moisture, not enough rain, lots of wind, and strange weather has been a part of global warming. Scientists are mixed up in the report they give about global warming. Some belief that it is here now and others believe it does not be a problem. The general population of Canada believes global warming is here and is a disasterous for our country. Gernerally Candians believe that it is the impact of fossil fuels which has caused global warming. Fossil fules are a major contributor to global warming. The use of oil, gas and coal is the enormous to fuel our transportation, warm our houses, and run our businesses. To begin with, oil is found in almost every area of our lifes. From the beginning of when we find oil to when we throw an oil product away we are adding to global warming. When they find oil, they get it out of the ground. When they get it out of the ground, the pollute the environment by using machinery. The machinery pollutes the air because the carbon monoxide is given off from the machines goes into our atmospere. If they are 'mining' the oil then large amounts of the land is destroyed and will take man, many years to grow again, Again the machinery that is used to strip the oil from the land pollutes the air with its carbon monoxide. The process that is used to take the oil out of the sand also pollutes the air. In addition to that, any of the products that are made from oil result in pollution in the way of factories putting smoke into the air. Natural gas is used to heat our homes and run some transportation. When natural gas is looked for, the process to look for it as pollution in the air because people drive around looking for where to find the natural gas. The natural gas also is taken from the ground using a process called fracking. This means that dirty water, chemicals and other stuffs are put into the ground to make natural gas, up out of the ground. All of this process creates pollution which goes into the atmosphere. Coal is used in Canada to make electricity. Coal is found in the ground and is mined and requires many big machines which run with oil. Of course, all of these big machines release carbon monoxide into the air. Huge coal burning factories make lots of pollution in the air while they are creating electricity to light everything that needs light. As a result of the coal burning so much in Canada, the pollution makes a hole in the ozone layer and the sun's rays heat the earth which creates global warming. Candidians really depend on fossil fuels. This dependent on fossil fuels makes Canada a big contributor to global warming. The conclusion we make is that Canadians need to look for other ways to create fuel, heat and light in the country. Canadians shouldn't be such huge contributors to global warming."



sample_sentence = "After they left on the bus, Mary and Samantha realized that Joe was waiting at the train station."
test_text = "I love her, but I don't know he loves me."
test_complex = "I can run faster than him. he is blackbird. I love many peoples. He is crying all day."


#------------------- first position ----------------
#type_percentage(text)

#------------------- second position ----------------
#number_different_words(text)

#------------------- third position ----------------
#number_complexwords(test_complex)

#------------------- fourth position ----------------
#relatedness_words(text)




#sent_tokenize_list = sent_tokenize(text)
#print(type_sentence(sample_sentence))

#pos_sentence = pos_vector(sample_sentence)
    
#key_text = "Lessee will have the right to place a sign on the front of the Premises"


#print(matching_rate(sentence, key_text), "----------matching rate-------------")

#gram_features(features, sentence)
#gram_features(features, key_text)

#pos_features(features, sample_sentence)

#sentiment_extract(features, sentence)

#capitalization(features,sentence)

#val = [i for i in features.values()]
#loaded_model = cPickle.load(open("model.pickle.dat", "rb"))
#y_pred = loaded_model.predict(val)

#print(y_pred)
