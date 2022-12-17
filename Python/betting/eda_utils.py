# -*- coding: utf-8 -*-
"""
TODO

:Author: Orestis Maroulis
:Created: 05/11/2021
:Copyright: 2021, Orestis Maroulis, All rights reserved.
"""


def momentum_logic(main_team_tier: int, other_team_tier: int, outcome: str) -> int:
    """
    Calculates the relative momentum of the team by looking at the previous lookback number of matches
    and assigning:
     -2 points if the ref team lost to a team of a lower rank
     -1 point if the ref team drew with a team of a lower rank
      0 points if the ref team drew with a team of the same rank
     +1 point if the ref team drew with a team of a higher rank
     +2 points if the ref team won against a team of a higher rank

    In all other cases, it is also 0.

     :param main_team_tier: the tier assigned to the main or reference team
     :param other_team_tier: the tier assigned to the opponent of the main team
     :param outcome: the outcome of the match
     :return: the score of after the logic has been applied according to the rules
     """
    # Validate outcome is as expected
    valid_outcomes = ['Draw', 'Win', 'Loss']

    if outcome not in valid_outcomes:
        raise ValueError(f'Wrong format/string for outcome. Expected any of {[*valid_outcomes]}')

    # try:
    if main_team_tier < other_team_tier:
        if outcome == 'Draw':
            score = 1
        elif outcome == 'Win':
            score = 2
        elif outcome == 'Loss':
            score = 0
    elif main_team_tier == other_team_tier:
        if outcome == 'Draw':
            score = 0
        elif outcome == 'Win':
            score = 1
        elif outcome == 'Loss':
            score = -1
    elif main_team_tier > other_team_tier:
        if outcome == 'Draw':
            score = -1
        elif outcome == 'Win':
            score = 0
        elif outcome == 'Loss':
            score = -2

    else:
        pass
    # except:
    #     raise Exception('Encountered problem with parsed tiers, please check.')

    return score

