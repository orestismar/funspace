import pandas as pd

from betting.basketball.data.utils import get_flashscore_basket_data, _cache_last_date


def test_get_flashscore_basket_data():
    flashscore_data = get_flashscore_basket_data(None)

    assert flashscore_data


# TODO do I still want this?
def test_match_data_scrap():
    match_url = 'https://www.flashscore.com/match/Mq8xrijR/#match-summary/point-by-point/0'
    assert True


def test_cache_last_date():
    test_tuple = ('Flashscore, Euroleague', pd.Timestamp.today())
    _cache_last_date(league_date_tuple=test_tuple)

    assert True
