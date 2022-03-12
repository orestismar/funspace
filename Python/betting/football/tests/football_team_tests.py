"""
Testing library from the football Team class.

:Author: Orestis Maroulis
:Created: 08/01/2022
:Copyright: 2022, Orestis Maroulis, All rights reserved.
"""

import numpy as np
import pandas as pd

from betting.football import FootballLeague, FootballTeam
from betting.football.football_leagues import football_leagues, ENGLAND_PREMIER
from betting.football.football_teams import LIVERPOOL


class TestTeam:

    def setup(self):
        # Set up the testing objects
        self.test_team = FootballTeam(LIVERPOOL)
        test_league = FootballLeague(
            name=ENGLAND_PREMIER,
            country=football_leagues[ENGLAND_PREMIER]
        )
        self.test_team.league = test_league

    def test_team_tier(self):
        test_tier = self.test_team.tier(num_tiers=4)
        assert isinstance(test_tier, (np.int64, int))

    def test_last_matches(self):
        test_last_3_matches = self.test_team.last_n_matches(n=3)
        test_last_week_matches = self.test_team.matches_last_week()

        assert isinstance(test_last_week_matches, pd.DataFrame)
        assert not test_last_week_matches.empty
        assert isinstance(test_last_3_matches, pd.DataFrame)
        assert not test_last_3_matches.empty

    def test_goals(self):
        assert self.test_team.goals_scored()
        assert self.test_team.goals_conceded()

    def test_relative_momentum(self):
        test_momentum = self.test_team.calculate_relative_momentum(num_rounds=4, num_tiers=4)

        assert isinstance(test_momentum[0], int) or isinstance(test_momentum[0], np.int64)
        assert isinstance(test_momentum[1], float)
