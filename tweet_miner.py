#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:16:37 2019

@author: nyjoey
"""

# Uncomment the lines below to store tweets into a csv

import tweepy
import csv #Import csv
consumer_key = "nI6iVCAbjsIxWe1H4zaiXutMD"
consumer_secret = "nC1MVxm1UVZxEwNGNMROKYMb3Ei4VF8jDm5pd3sj2lsml0UBDJ"
access_token = "1142633093590917122-jFZz9eyCzQYksrwGAzNNm0Ys56llWC"
access_token_secret = "cQhLvdGU8xxUFLfxZzM242a2BC8y580dmvV8xBwCkszMw"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

# Open/create a file to append data to a csv
csvFile = open('result.csv', 'a')

#Use csv writer
csvWriter = csv.writer(csvFile)

# Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets
public_tweets = api.home_timeline()
# foreach through all tweets pulled
for tweet in public_tweets:
   # printing the text stored inside the tweet object
   print(tweet.text)
   # Displays the time the tweets were created at
   print(tweet.created_at)
   # Name of the user
   print(tweet.user.screen_name)
   # Location of the user 
   
'''

   # Write a row to the CSV file. I use encode UTF-8
   csvWriter.writerow([tweet.text.encode('utf-8')])
   print(tweet.created_at, tweet.text)

'''


# This checks a twitter users tweets

# The Twitter user who we want to get tweets from
name = "LiquidHbox"
# Number of tweets to pull
tweetCount = 10000

# Calling the user_timeline function with our parameters
results = api.user_timeline(id=name, count=tweetCount)

# foreach through all tweets pulled
for tweet in results:
   # printing the text stored inside the tweet object
   print(tweet.text)
   

   # Write a row to the CSV file. I use encode UTF-8
   csvWriter.writerow([tweet.text.encode('utf-8')])
   print(tweet.created_at, tweet.text)


# This checks twitter based on a keyword 

# The search term you want to find
query = "Epilepsy"
# Language code (follows ISO 639-1 standards)
language = "en"

# Calling the user_timeline function with our parameters
results = api.search(q=query, lang="en")

# foreach through all tweets pulled
for tweet in results:
   # printing the text stored inside the tweet object
   print(tweet.user.screen_name,"Tweeted:",tweet.text)
   
'''  

    # Write a row to the CSV file. I use encode UTF-8
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    print(tweet.created_at, tweet.text)

'''

csvFile.close()