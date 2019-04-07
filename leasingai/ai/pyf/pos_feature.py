import nltk
from load_sentiment import load_sentiment

def pos_features(features,sentence):
    porter = nltk.PorterStemmer()
    sentiments = load_sentiment()
    sentence_rep = sentence
    token = nltk.word_tokenize(sentence_rep)
    token = [ porter.stem(each.lower()) for each in token]
    pos_vector = sentiments.pos_vector(token)
    for j in range(len(pos_vector)):
        features['POS_'+str(j+1)] = pos_vector[j]
    print ("done")

