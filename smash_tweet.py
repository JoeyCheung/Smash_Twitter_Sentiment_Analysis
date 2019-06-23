#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:16:37 2019

@author: nyjoey
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 
import re
import string
import pandas as pd
from textblob import TextBlob #trained on Stanford NLTK

def predict(tweet, custom_list):
    testimonial = TextBlob(tweet)
    polarity = testimonial.polarity
    
    for k in tweet.split():
        if k in custom_list:
            polarity = - 1
    return([polarity, testimonial.subjectivity])

# read data from file
data = pd.read_csv('result.csv')
data = data.values

output = []
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
custom_list = ["accident", "not", "confrontation"]
s = " "

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
 
# Combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

# Clean the data
for i,j in enumerate(data):
    temp = []
    tweet = re.sub('\[.*?\]', '', j[0]) # get rid of punctuations
    tweet = re.sub('[%s]' % re.escape(string.punctuation), '', tweet)
    tweet = re.sub('\w*\d\w*', '', tweet) # get rid of numbers
    tweet = re.sub('\W\w\W', '', tweet) 
    tweet = re.sub(r':', '', tweet) # Removes mentions 
    tweet = re.sub(r'‚Ä¶', '', tweet) # Removes RT
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet) #replace consecutive non-ASCII characters with a space
    tweet = emoji_pattern.sub(r'', tweet) # remove emojis from tweet
    tweet = word_tokenize(tweet)
    tweet = [porter.stem(word) for word in tweet] # stemming
    tweet = [lemmatizer.lemmatize(word) for word in tweet] # lemmatizing
    tweet = [word for word in tweet if word not in stop_words] # remove stop words
    tweet = s.join(tweet) # join tokens back to string. Textblob needs it in string
    if len(tweet) != 0:
        temp.append(data[i][0])
        temp += predict(tweet, custom_list)
        output.append(temp)

pd_data = pd.DataFrame(output)
pd_data.columns = ["Data", "Polarity", "Subjectivity"]
pd_data.to_csv('output.csv', encoding='utf-8', index=False)

for i in output:
    print(i)
