import sys
import json
import time
import logging
import twitter
import urllib.parse

from os import environ as e

print("hello world")

import tweepy
import csv

consumer_key = 'gm4REe8bvtAlUxzx3Db3xqlds'
consumer_secret = 's4XwBzozh4v3G935TCdvftp6j0Jc6KlRECHvHgm4kK4uBtU00s'
access_token = '3246640129-dViWYhgg99PQsspbgsk8ihM2Prgzg7lLfaWYilT'
access_token_secret = 'tRRy2d2GwBoPZROsHdHYbpAU1kaj4GyzVtPheoyaB5zJe'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Open/Create a file to append data

for tweet in tweepy.Cursor(api.search, q="#utah", count=100,
                           lang="en",
                           since="2019-04-15").items():
    print(tweet.created_at, tweet.id_str, tweet.source, tweet.text)
