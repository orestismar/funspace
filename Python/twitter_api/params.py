tweet_fields = 'author_id,created_at,text,entities,referenced_tweets,attachments,public_metrics'

query_params = {
    'start_time': '2017-01-01T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    'end_time': '2021-05-08T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    # 'start_time': '2017-01-01T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    # 'end_time': '2021-05-08T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    'tweet.fields': tweet_fields,
    'max_results': 500,  # This is the max results admitted by API endpoint
    'expansions': 'attachments.media_keys,author_id,geo.place_id',
    'media.fields': 'duration_ms,media_key,url,type,public_metrics',
    'user.fields': 'username',
}

# This is an example of multiple queries in same work. 
# TODO encrypt this
leader_id = 80820758
party_id = 4897361049

phrases = {
    # gets tweets of specified account, excludes retweets.
    "leader_acct": f'''from:{leader_id} -is:retweet''',
    "party_acct": f'''from:{party_id} -is:retweet'''
}

