"""
Summary:
This includes the websites addresses used in the scrapping applications


# Created by maror at 20/02/2021

"""
from enum import Enum


class SportsDataSites(Enum):
    """
    Enum to contain info and functionality of the websites used
    """
    oddsChecker = 'https://www.oddschecker.com/'
    who_scored_main = 'https://www.whoscored.com/'
    flashscore_main = 'https://www.flashscore.com'
