"""
Summary:
TODO

What would modelling depend on:
- Ranking
- Matches played last week
- Matches played last month
- Form - how to represent it?


Library defining utils and functionality specific to sport leagues.


# Created by maror at 17/04/2021

"""
import abc
import os
from functools import lru_cache
from typing import List

import pandas as pd

from betting.field_names import TIER, HOME, AWAY
from directories import BETTING_DATA_DIR

league_table = pd.DataFrame({'team': ['Arsenal', 'Wolves', 'Bolton', 'Liverpool']})
# todo for test only
DATA_LOCATION = BETTING_DATA_DIR


class League:
    """ Object containing functionality relevant to a Sports League """

    def __init__(self,
                 name: str,
                 country: str,
                 data_dir: str = DATA_LOCATION):
        self._name = name
        self.country = country
        self._teams: List = list()
        self._ranking_table: pd.DataFrame = pd.DataFrame()
        self.data_dir = data_dir

    @property
    def name(self):
        return self._name

    @property
    @lru_cache
    def teams(self):
        """ Sets the teams by picking the teams in the ranking table """
        return self.ranking_table['Team'].tolist()

    @property
    @lru_cache(maxsize=16)
    def ranking_table(self) -> pd.DataFrame:
        """ Gets and caches the ranking table by reading the corresponding sqlite file  """

        # TODO will need to reimplement for sqlite
        table = pd.read_excel(os.path.join(self.data_dir, f"{self.name}_ranking.xlsx"))

        return table

    @property
    def reg_season_rounds(self) -> int:
        """ Assuming all teams have to compete against each other """
        return (len(self.teams) - 1) * 2

    @property
    def num_teams(self) -> int:
        """ Returns the number of teams in the league """
        return len(self.teams)

    # TODO implement this
    def has_post_season(self) -> bool:
        raise NotImplementedError

    @lru_cache(maxsize=16)
    def league_matches_from_excel(self, team: str = None) -> pd.DataFrame:
        """
        :param team: the team to filter the league matches by
        :return:
        """

        filepath = os.path.join(DATA_LOCATION, f'{self.name}_matches.xlsx')
        # TODO will need to reimplement for sqlite
        league_matches = pd.read_excel(filepath)

        if team:
            return_df = league_matches[
                league_matches[HOME].str.contains(team) |
                league_matches[AWAY].str.contains(team)
                ]
        else:
            return_df = league_matches

        return return_df

    @lru_cache(maxsize=16)
    def tiered_league_table(self, num_tiers: int):
        """
        Gets the league table, index ranked, and assigns a tier to all teams in the league table

        :param num_tiers: the number of bins/tiers to split the teams into
        :return: df with the one more column, tier
        """

        tier_table = self.ranking_table.copy()
        tier_table[TIER] = pd.qcut(tier_table.index, q=num_tiers, labels=False)

        return tier_table


class Team:

    def __init__(self,
                 name: str,
                 ):
        self._league = None
        self._players_list = []
        self._tier: int = None
        self.name = name

    @property
    def players_list(self):
        raise NotImplementedError

    @property
    def league(self):
        return self._league

    @league.setter
    def league(self, value: League):
        self._league = value

    @property
    @lru_cache(maxsize=16)
    def all_matches(self) -> pd.DataFrame:
        all_matches: pd.DataFrame = self.league.league_matches_from_excel(team=self.name)

        # matches df may include future matches so use only the ones no later than today
        to_date_matches = all_matches[all_matches['Date'] <= pd.Timestamp.now()]
        return to_date_matches

    def last_n_matches(self, n: int) -> pd.DataFrame:
        """
        Slice the league's data to give only the requested last n number of matches of this team
        n: the number of last matches data to get
        :return: df of length n, with matches
        """

        last_matches = self.all_matches.sort_values(by=['Date']).tail(n)
        return last_matches

    def matches_last_week(self) -> pd.DataFrame:
        # get first and last datetime for final week of data
        range_max = self.all_matches['Date'].max()
        # Assuming month = 31 days
        range_min = range_max - pd.Timedelta(days=31)

        # take slice with final week of data
        last_week_matches = self.all_matches[
            (self.all_matches['Date'] >= range_min) &
            (self.all_matches['Date'] <= range_max)
            ]

        return last_week_matches

    @lru_cache
    def matches_last_month(self):
        # get first and last datetime for final month of data
        range_max = self.all_matches['Date'].max()
        range_min = range_max - pd.Timedelta(days=1)

        # take slice with final week of data
        last_week_matches = self.all_matches[
            (self.all_matches['Date'] >= range_min) &
            (self.all_matches['Date'] <= range_max)
            ]

        return last_week_matches

    def weighted_form(self):
        """
        This uses the last matches to derive the weighted form by scaling the outcomes and goals according to
        the opponent team's strength
        :return:
        """

        raise NotImplementedError

    @property
    def number_of_injuries(self):
        raise NotImplementedError

    @property
    def changed_coach_last_month(self):
        raise NotImplementedError

    def tier(self, num_tiers: int = 3) -> int:
        """
        Get the tier of self compared to the rest of the teams in the league
        :return: tier
        """
        if not self._tier:
            tiered_table = self.league.tiered_league_table(num_tiers=num_tiers).set_index('Team')
            self._tier = tiered_table[TIER].loc[self.name]

        return self._tier

    @abc.abstractmethod
    def calculate_relative_momentum(self, num_rounds: int, num_tiers: int = 3) -> (int, float):
        pass


class Player:
    def __init__(self):
        raise NotImplementedError

    pass


def validate_ranking_table():
    """ Makes sure that the matches played shown in the ranking table match the number of matches found in the results'
     database per team """

    pass
