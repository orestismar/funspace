"""
Testing library from the football utils module.

:Author: Orestis Maroulis
:Created: 06/02/2022
:Copyright: 2022, Orestis Maroulis, All rights reserved.
"""
import pandas as pd

from betting.football import FootballLeague
from betting.football.football_leagues import ENGLAND_PREMIER, football_leagues
from betting.football.utils import analyse_next_games, calculate_stats_for_matches


def test_analyse_next_games():
    test_league = FootballLeague(
        name=ENGLAND_PREMIER,
        country=football_leagues[ENGLAND_PREMIER]
    )

    test_result = analyse_next_games(league=test_league,
                                     days_to_analyse=2,
                                     num_tiers=3)

    assert isinstance(test_result, pd.DataFrame)
    assert not test_result.empty


def test_calculate_stats_for_matches():

    test_league = FootballLeague(
        name=ENGLAND_PREMIER,
        country=football_leagues[ENGLAND_PREMIER]
    )

    last_matches = test_league.league_matches_from_excel().head(30)

    test_stats = calculate_stats_for_matches(matches_info=last_matches)

    assert not test_stats.empty

    assert not test_stats.isna().any()
