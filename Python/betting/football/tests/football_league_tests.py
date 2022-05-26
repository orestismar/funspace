"""
Testing library from the football league class.

:Author: Orestis Maroulis
:Created: 08/01/2022
:Copyright: 2022, Orestis Maroulis, All rights reserved.
"""

import pandas as pd

from betting.football import FootballLeague
from betting.football.football_leagues import football_leagues, ENGLAND_PREMIER


class TestFootballLeague:

    def setup(self):
        # Set up the testing objects
        self.test_league = FootballLeague(
            name=ENGLAND_PREMIER,
            country=football_leagues[ENGLAND_PREMIER]
        )

    # TEST LEAGUE
    def test_ranking_table(self):
        test_ranking_table = self.test_league.ranking_table
        assert isinstance(test_ranking_table, pd.DataFrame)
        assert not test_ranking_table.empty

    def test_teams(self):
        test_teams = self.test_league.teams

        assert isinstance(test_teams, list)
        assert test_teams

    def test_tiered_table(self):
        test_tiered_table = self.test_league.tiered_league_table(num_tiers=2)
        assert isinstance(test_tiered_table, pd.DataFrame)
        assert not test_tiered_table.empty

    def test_league_matches(self):
        test_league_matches = self.test_league.league_matches_from_excel()
        assert isinstance(test_league_matches, pd.DataFrame)
        assert not test_league_matches.empty

    pass
