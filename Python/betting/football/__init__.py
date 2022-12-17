from abc import ABC

import pandas as pd

from betting.eda_utils import momentum_logic
from betting.field_names import TIER, HOME, AWAY
from betting.team import League, Player, Team


class FootballLeague(League, ABC):
    def __init__(self, name: str, country: str):
        super().__init__(name, country)

    @property
    def rounds(self):
        raise NotImplementedError

    @property
    def champions_league_places(self):
        raise NotImplementedError

    @property
    def europa_league_places(self):
        raise NotImplementedError

    @property
    def relegations_places(self):
        raise NotImplementedError

    @property
    def whoscored_url(self):
        raise NotImplementedError


class FootballTeam(Team, ABC):

    def __init__(self,
                 name: str):
        super().__init__(name=name)
        self.goals: pd.DataFrame = pd.DataFrame()

    def calculate_relative_momentum(self, num_rounds: int, num_tiers: int = 3) -> (int, float):
        """
        Calculates the relative momentum score of the given team by working out the outcome of the last n_rounds and then
        calculating the tier of each opponent and applying the logic outlined in the momentum_logic function.

        :param num_rounds: the number of rounds to take into account when calculating the momentum
        :param num_tiers:  number of tiers to take into account when calculating the momentum
        :return: a tuple including an integer score for the relative momentum/form score and a float for
            the rel form standard deviation
        """

        # New Column names
        opponent = 'Opponent'
        outcome = 'Outcome'
        is_home = 'Is_Home_Team'

        # Get last num_rounds data
        match_data: pd.DataFrame = self.last_n_matches(n=num_rounds)

        team_tier = self.tier()

        # Add the tiers of the opponents
        # Opponent is the team against "team" arg is competing against
        # TODO make sure the names of the columns match conventions here - how to avoid hard-coded
        # TODO maybe by using the expected naming in the args?
        match_data[opponent] = None
        match_data.loc[match_data[HOME] != self.name, opponent] = match_data[HOME]
        match_data.loc[match_data[AWAY] != self.name, opponent] = match_data[AWAY]

        # Get the tiered table and join the rank column
        tiered_league_table = self.league.tiered_league_table(num_tiers=num_tiers)

        match_data_w_tier = match_data.merge(
            right=tiered_league_table[['Team', TIER]],
            how='left',
            left_on=opponent,
            right_on='Team',
        )

        # Add is_home column
        match_data_w_tier[is_home] = match_data_w_tier[HOME] == self.name

        match_data_w_tier[outcome] = match_data_w_tier.apply(
            lambda x: outcome_logic(x["Home Goals"], x["Away Goals"], x[is_home]), axis=1)

        ref_team_form = match_data_w_tier.apply(
            lambda x: momentum_logic(team_tier, x[TIER], x[outcome]), axis=1)

        ref_team_form_score: int = ref_team_form.sum()
        ref_team_form_std: float = ref_team_form.std()

        return ref_team_form_score, ref_team_form_std

    def goals_scored(self, num_matches: int = None):
        """

        :param num_matches: number of last matches' goals to return
        :return:
        """
        if 'Scored' not in self.all_matches.columns:
            home_idx = self.all_matches.loc[self.all_matches['Home Team'] == self.name].index
            away_idx = self.all_matches.loc[self.all_matches['Away Team'] == self.name].index

            self.all_matches.loc[home_idx, 'Scored'] = self.all_matches['Home Goals']
            self.all_matches.loc[away_idx, 'Scored'] = self.all_matches['Away Goals']

        # if requested goals for specific number of matches only
        if not num_matches:
            goals_scored = self.all_matches['Scored'].sum()
        else:
            goals_scored = self.all_matches['Scored'].tail(num_matches).sum()

        return goals_scored

    def goals_conceded(self, num_matches: int = None):
        """

        :param num_matches: number of last matches' goals to return
        :return:
        """
        if 'Conceded' not in self.all_matches.columns:
            home_idx = self.all_matches.loc[self.all_matches['Home Team'] == self.name].index
            away_idx = self.all_matches.loc[self.all_matches['Away Team'] == self.name].index

            self.all_matches.loc[home_idx, 'Conceded'] = self.all_matches['Away Goals']
            self.all_matches.loc[away_idx, 'Conceded'] = self.all_matches['Home Goals']

        # if requested goals for specific number of matches only
        if not num_matches:
            goals_scored = self.all_matches['Conceded'].sum()
        else:
            goals_scored = self.all_matches['Conceded'].tail(num_matches).sum()

        return goals_scored

    @property
    def plays_cl(self) -> bool:
        """If the team has played a champions league match in the last month"""

        raise NotImplementedError


class FootballPlayer(Player):
    # todo - we will want to get the main stats of the players of each team, and store them in different attributes

    def __init__(self):
        super().__init__()
        raise NotImplementedError

    pass


def outcome_logic(home_goals: int,
                  away_goals: int,
                  outcome_for_home: bool) -> str:
    """

    Returning an outcome string depending on the goals for and against

    :param home_goals: number of goals scored by the home team
    :param away_goals: number of goals scored by the away team
    :param outcome_for_home: true if the team of interest is the home team in this match, false otherwise
    :return: Loss, Win or Draw
    """

    if home_goals == away_goals:
        outcome = 'Draw'
    elif home_goals > away_goals:
        if outcome_for_home:
            outcome = 'Win'
        else:
            outcome = 'Loss'
    else:
        if outcome_for_home:
            outcome = 'Loss'
        else:
            outcome = 'Win'

    return outcome
