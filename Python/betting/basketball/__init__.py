"""

Functionality for analysis of the basketball data in our disposal

1. read the data
2. split the dataset by league? or other
3.

"""
from abc import ABC

import sklearn

from betting.team import League


class Match:

    # todo we can use the downloaded data for this
    def __init__(self):
        # todo
        pass

    @property
    def datetime(self):
        return 0

    @property
    def home_team(self):
        return 0

    @property
    def away_team(self):
        return 0

    @property
    def total_home_points(self):
        return 0

    @property
    def total_away_points(self):
        return 0

    @property
    def quarter1_home_points(self):
        return 0

    @property
    def quarter1_away_points(self):
        return 0

    @property
    def quarter2_home_points(self):
        return 0

    @property
    def quarter2_away_points(self):
        return 0

    @property
    def quarter3_home_points(self):
        return 0

    @property
    def quarter3_away_points(self):
        return 0

    @property
    def quarter4_home_points(self):
        return 0

    @property
    def quarter4_away_points(self):
        return 0

    pass


class BasketballLeague(League, ABC):
    def __init__(self, name: str, country: str):
        super().__init__(name, country)

    pass