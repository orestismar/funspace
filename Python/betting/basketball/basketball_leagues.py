from abc import ABC
from enum import Enum
from typing import List

from betting.basketball import Match
from betting.team import Team, League


class FlashscoreBasketLeagues(Enum):
    """ Main basketball league titles on FlashScore """
    Greece = 'GREECE: Basket League'
    Spain = 'SPAIN: ACB'
    France = 'FRANCE: LNB'
    Italy = 'ITALY: Lega A'
    Turkey = 'TURKEY: Super Lig'
    Euroleague = 'EUROPE: Euroleague'
    Eurocup = 'EUROPE: Eurocup'
    ChampionsLeague = 'EUROPE: Champions League'


class BasketballTeam(Team, ABC):

    def __init__(self):
        super().__init__()
        self._international_league = None

    def points_scored(self, for_all_matches: bool = True, last_matches: int = 0):

        if for_all_matches and last_matches:
            raise ValueError('Cannot return points scored for all matches when given last_matches value.'
                             ' Please choose only one and try again.')

        raise NotImplementedError

    def points_conceded(self, for_all_matches: bool = True, last_matches: int = 0):
        if for_all_matches and last_matches:
            raise ValueError('Cannot return points scored for all matches when given last_matches value.'
                             ' Please choose only one and try again.')

        raise NotImplementedError

    @property
    def international_league(self):
        """
        The national league in which the team competes
        """
        return self._international_league

    @international_league.setter
    def league(self, league: League):
        self._international_league = league

    def all_matches(self) -> List[Match]:
        """
        Returns a list of Match objects for the specific team
        # TODO consider year for future?
        :return:
        """

    def national_matches(self) -> List[Match]:
        """
        Returns a list of Match objects for team in its national League
        # TODO consider year for future?
        :return:
        """

    def international_matches(self) -> List[Match]:
        """
        Returns a list of Match objects for team in its international League
        # TODO consider year for future?
        :return:
        """

    def roster(self):
        """
        The players of the team
        :return:
        """

    def average_total_scoring(self):
        """ Average of full time points scored against any team """

    def average_total_scoring_vs_lower_rank(self, national_league: bool):
        """ Average of full time points scored against lower ranked teams """

    def average_total_scoring_vs_medium_rank(self, national_league: bool):
        """ Average of full time points scored against medium ranked teams """

    def average_total_scoring_vs_higher_rank(self, national_league: bool):
        """ Average of full time points scored against medium ranked teams """

    pass