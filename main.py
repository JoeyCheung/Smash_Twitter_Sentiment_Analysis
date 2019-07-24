import pandas as pd
from textblob import TextBlob #trained on Stanford NLTK
import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
from collections import Counter, OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob.sentiments import NaiveBayesAnalyzer
import time
os.system('clear')

start = time.time()

inputFilename = 'label.csv'
outputFilename = 'combinedData_output.csv'

data = pd.read_csv(inputFilename, header=None)
data = data.values[1:]


def wordCounterGlove():
    """
    Get a corpus of valid words
    """
    text = (open('glove_words_840B.txt','r')).read()
    words = re.findall(r'\w+', text.lower())
    wordTypes_n_counts = Counter(words) # types = 32198, tokens = 1115585
    return wordTypes_n_counts

def predictPolaritySubjectivity(text, custom_list):
    testimonial = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    polarity = testimonial.polarity
    
    for k in text.split():
        if k in custom_list:
            polarity = - 1
    return([polarity, testimonial.subjectivity])

lemmatizer = WordNetLemmatizer()
#validTokens = wordCounter().keys()
validTokens = wordCounterGlove().keys()
stop_words = stopwords.words('english')


positiveCorpus = []
negativeCorpus = []

for index,sample in enumerate(data):
    temp = word_tokenize(str(sample))
    #temp = [lemmatizer.lemmatize(token.lower()) for token in temp]
    temp = [lemmatizer.lemmatize(token) for token in temp]
    temp = [word for word in temp if word in validTokens and 
                                len(word) > 2 and word.isalpha()]
    temp = [word for word in temp if word not in stop_words]
    result = predictPolaritySubjectivity(" ".join(temp), [])
    #print(result)
    if index == 1:
        print(result[0])
    if result[0] + 0.3 > result[1]:
        positiveCorpus += temp
    else:
        negativeCorpus += temp

print(len(positiveCorpus))
print(len(negativeCorpus))
vectorizer = TfidfVectorizer()
corpus = []
corpus.append(" ".join(positiveCorpus))
corpus.append(" ".join(negativeCorpus))
tfidf_matrix = vectorizer.fit_transform(corpus)
df = pd.DataFrame(tfidf_matrix.toarray(), columns = vectorizer.get_feature_names())
df.to_csv(outputFilename)

end = time.time()
print(end - start)
