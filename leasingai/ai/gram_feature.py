import nltk


def gram_features(features,sentence):
    porter = nltk.PorterStemmer()
    sentence_rep = sentence
    token = nltk.word_tokenize(sentence_rep)
    token = [porter.stem(i.lower()) for i in token]        
    
    bigrams = nltk.bigrams(token)
    bigrams = [tup[0] + ' ' + tup[1] for tup in bigrams]
    grams = token + bigrams

