import string
import nltk
from .load_sentiment import load_sentiment

def sentiment_extract(features, sentence):
    porter = nltk.PorterStemmer()
    sentiments = load_sentiment()
    sentence_rep = sentence
    token = nltk.word_tokenize(sentence_rep)    
    token = [porter.stem(i.lower()) for i in token]   
    mean_sentiment = sentiments.score_sentencce(token)
    features["Positive Sentiment"] = mean_sentiment[0]
    features["Negative Sentiment"] = mean_sentiment[1]
    features["sentiment"] = mean_sentiment[0] - mean_sentiment[1]    
    try:
        text = TextBlob(" ".join([""+i if i not in string.punctuation and not i.startswith("'") else i for i in token]).strip())
        features["Blob Polarity"] = text.sentiment.polarity
        features["Blob Subjectivity"] = text.sentiment.subjectivity
    except:
        features["Blob Polarity"] = 0
        features["Blob Subjectivity"] = 0
        print("do nothing")                
    first_half = token[0:len(token)//2]            
    mean_sentiment_half = sentiments.score_sentencce(first_half)
    features["positive Sentiment first half"] = mean_sentiment_half[0]
    features["negative Sentiment first half"] = mean_sentiment_half[1]
    features["first half sentiment"] = mean_sentiment_half[0]-mean_sentiment_half[1]
    try:
        text = TextBlob(" ".join([""+i if i not in string.punctuation and not i.startswith("'") else i for i in first_half]).strip())
        features["first half Blob Polarity"] = text.sentiment.polarity
        features["first half Blob Subjectivity"] = text.sentiment.subjectivity
    except:
        features["first Blob Polarity"] = 0
        features["first Blob Subjectivity"] = 0
    second_half = token[len(token)//2:]
    mean_sentiment_sechalf = sentiments.score_sentencce(second_half)
    features["positive Sentiment second half"] = mean_sentiment_sechalf[0]
    features["negative Sentiment second half"] = mean_sentiment_sechalf[1]
    features["second half sentiment"] = mean_sentiment_sechalf[0]-mean_sentiment_sechalf[1]
    try:
        text = TextBlob(" ".join([""+i if i not in string.punctuation and not i.startswith("'") else i for i in second_half]).strip())
        features["second half Blob Polarity"] = text.sentiment.polarity
        features["second half Blob Subjectivity"] = text.sentiment.subjectivity
    except:
        features["second Blob Polarity"] = 0
        features["second Blob Subjectivity"] = 0

