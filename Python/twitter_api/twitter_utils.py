"""
Summary: module with utils function to be used in calling twitter API calls


# Created by maror at 14/03/2021

"""

import csv
import os
from typing import Dict
import pandas as pd
from directories import _temp_dir


def write_dict_to_csv(dict: Dict, csv_filename: str):
    """TODO"""

    try:
        with open(csv_filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile)  # , fieldnames=csv_columns)
            writer.writeheader()
            for data in dict:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def extract_tweets_from_response(response_dic: Dict) -> pd.DataFrame:
    """
    :param response_dic: a response dictionary with 'data' and 'meta' as keys. Within the data key value there is a list
     and within it another dictionary with 'id' and 'text' as keys. The 'text' value is the actual tweet
    :return: pd.Series of tweets
    """

    response_list_of_dicts = response_dic['data']

    # id_idx, tweets = [], []
    #
    # for tweet_object in response_list_of_dicts:
    #     # Append tweeter id and tweet to relevant lists
    #     id_idx.append(tweet_object['id'])
    #
    #     tweets.append(tweet_object['text'])

    tweets_df = pd.DataFrame(data=response_list_of_dicts)

    return tweets_df


def write_tweets_to_excel(tweet_df: pd.DataFrame, name: str):
    """
    Writes an excel in C:\\temp with the twitter series
    :return:
    """

    file_name = f'''Tweets_{name}_{pd.Timestamp.today().date()}.xlsx'''
    file_path = os.path.join(_temp_dir, file_name)

    # write it
    tweet_df.to_excel(file_path)

    pass
