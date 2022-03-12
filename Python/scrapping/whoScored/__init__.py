"""
Summary:
Init file with class and methods to get football data from whoScored.com

# Created by maror at 20/02/2021

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import calendar
import time
import enum
import requests
from bs4 import BeautifulSoup
from betting.football.football_countries import *

who_scored_main = 'https://www.whoscored.com/'


class whoScored:
    def __init__(self):
        # @TODO why do we need this?
        self.url = self._get_team_page()
        self._soup = None

    def _get_team_page(self, number: int = 167, country: str = england, team: str = liverpool):
        """
        @TODO documentation
        :param number:
        :param country:
        :param team:
        :return:
        """
        # example page: https://www.whoscored.com/Teams/167/Show/England - Manchester - City

        # if team name has a gap pre-process with dash
        team = team.replace(' ', '-')

        team_page = f'{who_scored_main}Teams/{number}/Show/{country}-{team}'

        return team_page
