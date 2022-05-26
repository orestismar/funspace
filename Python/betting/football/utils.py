"""
TODO

"""
from statistics import mean, stdev
from typing import Union

import pandas as pd

from betting.football import FootballLeague, FootballTeam


def analyse_next_games(
        league: FootballLeague,
        days_to_analyse: int = 3,
        num_tiers: int = 4

) -> pd.DataFrame:
    """
    TODO
    :param league:
    :param days_to_analyse:
    :param num_tiers:
    :return:
    """
    # Get all matches and pick the next
    all_matches = league.league_matches_from_excel()
    upcoming_matches = all_matches.loc[(all_matches['Date'] >= pd.Timestamp.today()) &
                                       (all_matches['Date'] <= pd.Timestamp.today() + pd.Timedelta(days=days_to_analyse)
                                        )
                                       ]

    # List to contain dicts with the stats of the home and away teams for each upcoming match with len(upcoming_matches)
    upcoming_matches_stats_list = []
    for index, row in upcoming_matches.iterrows():
        # Create objects for home and away teams
        home_team = FootballTeam(name=row['Home Team'])
        away_team = FootballTeam(name=row['Away Team'])
        # Set the same league - the one we are concerned in here - for both
        home_team.league, away_team.league = league, league

        # Get stats
        upcoming_matches_stats_list.append(get_upcoming_match_analysis(home_team=home_team,
                                                                       away_team=away_team,
                                                                       league=league,
                                                                       num_tiers=num_tiers))

    matches_df = upcoming_matches_stats_list[0]  # by default the first one
    for df in upcoming_matches_stats_list[1:]:
        matches_df = matches_df.join(df)

    return matches_df


# TODO add more stats
def get_upcoming_match_analysis(home_team: FootballTeam,
                                away_team: FootballTeam,
                                league: FootballLeague,
                                num_tiers: int = 3
                                ) -> pd.DataFrame:
    """
    Given the home and away team, output a dictionary with the main stats/analysis

    :param home_team: the home team of the match
    :param away_team: the away team of the match
    :param league: the league where they compete
    :param num_tiers: how many tiers to split the league to
    :return: Multi-column dataframe with match/team in columns
    """

    home_team.league = league
    away_team.league = league

    # Stats to calculate: momentum (5 and 3 rounds),
    # avg and std of goals scored/conceded in last 3 matches home and away

    team_stats = {}
    for team in [home_team, away_team]:
        team_stats[team.name] = {
            '5r_relative_momentum': team.calculate_relative_momentum(num_rounds=5, num_tiers=num_tiers),
            '3r_relative_momentum': team.calculate_relative_momentum(num_rounds=3, num_tiers=num_tiers),
            '3r_avg_goals_scored': mean([
                team.goals_scored(num_matches=1),
                team.goals_scored(num_matches=2),
                team.goals_scored(num_matches=3)]),
            '3r_avg_goals_conceded': mean([
                team.goals_conceded(num_matches=1),
                team.goals_conceded(num_matches=2),
                team.goals_conceded(num_matches=3)]),
            '3r_std_goals_scored': stdev([
                team.goals_scored(num_matches=1),
                team.goals_scored(num_matches=2),
                team.goals_scored(num_matches=3)]),
            '3r_std_goals_conceded': stdev([
                team.goals_conceded(num_matches=1),
                team.goals_conceded(num_matches=2),
                team.goals_conceded(num_matches=3)]),
            '3r_goals_scored_range': (
                min(team.goals_scored(num_matches=1),
                    team.goals_scored(num_matches=2),
                    team.goals_scored(num_matches=3)),
                max(team.goals_scored(num_matches=1),
                    team.goals_scored(num_matches=2),
                    team.goals_scored(num_matches=3))),
            '3r_goals_conceded_range': (
                min(team.goals_conceded(num_matches=1),
                    team.goals_conceded(num_matches=2),
                    team.goals_conceded(num_matches=3)),
                max(team.goals_conceded(num_matches=1),
                    team.goals_conceded(num_matches=2),
                    team.goals_conceded(num_matches=3))),

        }

    # Convert to Multi index dataframe
    team_stats_df = pd.DataFrame(team_stats).T

    team_stats_df['match'] = "-".join([home_team.name, away_team.name])
    team_stats_df.set_index([team_stats_df['match'], team_stats_df.index], inplace=True)
    team_stats_df.drop(columns=['match'], inplace=True)

    # transpose again to have match/teams in multi-index columns and return
    return_df = team_stats_df.T
    return return_df


# TODO try a dict/class where is stat has it's associated operation, e.g. Total Goals > x, and abstract it
#  by just applying the operation in this function
def calculate_stats_for_matches(matches_info: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
    """
    By default calculates the percentages of matches in the matches_info for over2.5, over3.5, goal-goal,
    goal and over2.5
    :param matches_info: matches dataframe
    :return: series with percentage of TRUE for all the stats in stats_to_calc
    """

    # Include more stats as needed
    stats_to_calc = ['is_goal', 'over25', 'over35', 'goal_and_over25']

    # New columns and set to False
    for stat in stats_to_calc:
        matches_info[stat] = False

    # Update where it's true
    is_goal_idx = matches_info.loc[(matches_info['Home Goals'] > 0) &
                                   (matches_info['Away Goals'] > 0)].index
    matches_info.loc[is_goal_idx, 'is_goal'] = True

    matches_info['Total Goals'] = matches_info['Home Goals'] + matches_info['Away Goals']
    over25_idx = matches_info.loc[matches_info['Total Goals'] > 2.5].index
    over35_idx = matches_info.loc[matches_info['Total Goals'] > 3.5].index

    matches_info.loc[over25_idx, 'over25'] = True
    matches_info.loc[over35_idx, 'over35'] = True

    goal_and_over25_idx = matches_info.loc[(matches_info['is_goal']) &
                                           (matches_info['over25'])].index

    matches_info.loc[goal_and_over25_idx, 'goal_and_over25'] = True

    # Calculate % of the stats column where they are TRUE
    matches_stats = matches_info[stats_to_calc]

    matches_stats_summary = matches_stats.sum() / len(matches_stats)

    return matches_stats_summary
