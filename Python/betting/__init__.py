"""

Summary:
TODO

# Created by maror on 12/02/2022
"""
from abc import ABC
from datetime import datetime
from typing import Union

import pandas as pd

from betting.team import Team


class Match:
    """ A sports match abstract class. Will be implemented by concrete classes per specific sport. """

    def __init__(self,
                 date: Union[datetime, pd.datetime],
                 home_team: Team,
                 away_team: Team):
        self._date = date
        self._home_team: Team = home_team
        self._away_team: Team = away_team


class FootballMatch(Match, ABC):
    """ Concrete class implementing a football match """

    def __init__(self,
                 date: Union[datetime, pd.datetime],
                 home_team: Team,
                 away_team: Team):
        super().__init__(date=date, home_team=home_team, away_team=away_team)

    def is_goal_goal(self):
        pass

    def is_goal_and_over2(self):
        pass

    def is_over2(self):
        pass

    pass
