# -*- coding: utf-8 -*-
"""
Created on Mon May  4 22:42:03 2020

WIP ==

This is an instagram bot program using instapy package

@author: maror

"""

from instapy import InstaPy
from typing import List

# TODO really need to encrypt these before uploading
user = 'orestismar'
acct_password = 'souzy2104'


def insta_session(username: str,
                  password: str,
                  num_posts_to_like: int = 20,
                  pct_posts_to_follow: float = 40,
                  like_tags: List[str] = ["travel", "nature", "holidays"],
                  auto_comment: bool = False,
                  auto_comment_pct: float = 50,
                  auto_comment_list: List[str] = ["Nice!", "Sweet!", "Beautiful :heart_eyes:"],
                  max_followers: int = 10000):
    session = InstaPy(username=username, password=password).login()

    session.login()

    # what hashtags to like + amount
    session.like_by_tags(like_tags, amount=num_posts_to_like)

    # don't like posts with these tags
    session.set_dont_like(["naked", "nsfw", "gay", "sex"])

    # follow some of the posts you like (set percentage)
    session.set_do_follow(True, percentage=pct_posts_to_follow)

    # Auto commenting
    if auto_comment:
        session.set_do_comment(True, percentage=auto_comment_pct)
        session.set_comments(auto_comment_list)

    # Do not like if they have more than xxx followers
    session.set_relationship_bounds(enabled=True, max_followers=max_followers)

    # TODO do I need to adjust these?
    session.set_quota_supervisor(enabled=True, peak_comments_daily=240, peak_comments_hourly=21)

    # TODO maybe implement some AI here for more analysis
    # session.set_use_clarifai(enabled=True, api_key='<your_api_key>')
    # session.clarifai_check_img_for(['nsfw'])

    # end session
    session.end()

    pass


if __name__ == '__main__':

    try:

        insta_session(username=user,
                      password=acct_password)

        print('Completed successfully')

    except:
        print('Error. Process not completed.')
