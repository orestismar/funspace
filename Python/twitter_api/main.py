from twitter_api.params import query_params, phrases
import twitter_api.query as q
from twitter_api.twitter_utils import extract_tweets_from_response, write_tweets_to_excel
import time
import pandas as pd

# TODO encrypt this
bearer_token = "AAAAAAAAAAAAAAAAAAAAAE6RPQEAAAAAiwi%2BYVGJkp1GH2cLc5fO%2Fr5X68k%3DMMapD41fEidxeL0xlMjrn3JcCvh0yCRCCN6xaz9Di2LE0xqIk3"

dfs_dict = {}


def loop(headers, query_params, pagination_token, loop_counter):
    json_response = q.query_loop(headers, query_params, pagination_token)
    dfs_dict[f'pagination{loop_counter}'] = extract_tweets_from_response(json_response)

    # dumper.save_data(json_response, loop_counter, phrase)
    try:
        if json_response["meta"]["next_token"]:
            pagination_token = json_response["meta"]["next_token"]
            # New API V2 require pagination for each 500 results. Here we get the pagination token.
            time.sleep(4)  # THIS AVOID HIT RATE LIMIT (300 Requests in a 15 Min Window)
            print("sleeping for 4 sec")
            loop_counter += 1
            loop(headers, query_params, pagination_token, loop_counter)
    except KeyError:
        print("Last Page")


def main():
    loop_counter = 1

    # Run for the different query phrases
    for phrase_key in phrases.keys():

        # Clear dictionary and start anew
        dfs_dict.clear()

        phrase = phrases[phrase_key]

        headers = q.create_headers(bearer_token)
        query_params["query"] = phrase
        json_response = q.query(headers, query_params)

        # extract first tweets to dfs_dict
        dfs_dict[f'pagination{loop_counter}'] = extract_tweets_from_response(json_response)

        # dumper.save_data(json_response, loop_counter, phrase)

        # todo do the looping better
        try:
            if json_response["meta"]["next_token"]:
                pagination_token = json_response["meta"]["next_token"]
                loop_counter += 1
                time.sleep(4)  # THIS AVOID HIT RATE LIMIT (300 Requests in a 15 Min Window)
                print("sleeping for 4 sec")
                loop(headers, query_params, pagination_token, loop_counter)
        except KeyError:
            print("Last Page")

        # Consolidate dfs in dict into one
        dfs_list = list()
        for key in dfs_dict.keys():
            dfs_list.append(dfs_dict[key])

        master_df = pd.concat(dfs_list)

        write_tweets_to_excel(master_df, phrase_key)
        pass


if __name__ == "__main__":
    main()
