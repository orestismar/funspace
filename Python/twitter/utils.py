"""
Summary:
Utilities for the twitter package

Created by maror at 11/06/2022
"""
import os.path
from enum import Enum
from typing import Dict

import pandas as pd
import requests
import tweepy

from directories import _C_DIR

CREDENTIALS_PATH = os.path.join(_C_DIR, 'protected_credentials\OM_twitter_credentials.txt')


class TwitterCredentials(Enum):
    BearerToken = 'Bearer Token'
    ConsumerKey = 'API Key'
    ConsumerSecret = 'API Key Secret'
    AccessToken = 'Access Token'
    AccessTokenSecret = 'Access Token Secret'


def get_credentials(filepath: str = CREDENTIALS_PATH) -> Dict[str, str]:
    credentials: Dict = {}
    with open(filepath) as f:
        contents = f.readlines()
        for line in contents:
            key, value = line.rstrip('\n').split(":")[0], line.rstrip('\n').split(":")[1]
            credentials[key] = value

    return credentials


def get_tweets():
    """
    TODO
    :return:
    """

    credentials: Dict = get_credentials(filepath=CREDENTIALS_PATH)
    client = tweepy.Client(bearer_token=credentials.get(TwitterCredentials.BearerToken.value),
                           consumer_key=credentials.get(TwitterCredentials.ConsumerKey.value),
                           consumer_secret=credentials.get(TwitterCredentials.ConsumerSecret.value),
                           access_token=credentials.get(TwitterCredentials.AccessToken.value),
                           access_token_secret=credentials.get(TwitterCredentials.AccessTokenSecret.value),
                           return_type=requests.Response,
                           wait_on_rate_limit=True)

    # Define query
    query = 'crypto -is:retweet'

    # get max. 100 tweets
    tweets = client.search_recent_tweets(query=query,
                                         max_results=10)

    # Save data as dictionary
    tweets_dict = tweets.json()

    # Extract "data" value from dictionary
    tweets_data = tweets_dict['data']

    # Transform to pandas Dataframe
    df = pd.json_normalize(tweets_data)

    return df


def test_query():
    """ TODO"""
    test_result = get_tweets()
    assert not test_result.empty


def test_get_credentials():
    test_data = get_credentials()
    assert test_data
