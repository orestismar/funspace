"""
Summary:
Example of a full archive search

Created by maror at 11/06/2022
"""

import json
import os

import requests

FULL_ARCHIVE_URL = "https://api.twitter.com/2/tweets/search/all"

bearer_token = os.environ.get("BEARER_TOKEN")

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    'query': '(from:twitterdev -is:retweet)',
    # 'tweet.fields': 'author_id',
    # 'max_results': 10
}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", FULL_ARCHIVE_URL, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    json_response = connect_to_endpoint(url=FULL_ARCHIVE_URL, params=query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
