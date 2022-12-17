"""

Automate scrapping from Flash Score
"""

import os

import pandas as pd

from betting.basketball.data.utils import get_flashscore_basket_data, logger
from betting.basketball.basketball_leagues import FlashscoreBasketLeagues
from directories import _TMP

# TODO - include this date in the logic - maybe read the last date from excel/database
last_cached_date = None

leagues_to_get = [
    FlashscoreBasketLeagues.Greece.value,
    FlashscoreBasketLeagues.Spain.value,
    FlashscoreBasketLeagues.France.value,
    FlashscoreBasketLeagues.Italy.value,
    FlashscoreBasketLeagues.Turkey.value,
    FlashscoreBasketLeagues.Euroleague.value
    # TODO add missing
]


def main():
    try:
        basket_data, missing_data = get_flashscore_basket_data(league_list=leagues_to_get)

        # TODO cache/save the latest date games so that we don't have to copy everything every time
        # TODO we also need a way to update the data set in this case

        # Write the data to an excel file
        games_file_name = f'''FlashScore_{pd.Timestamp.today().strftime('%d%m%y_%H%M')}.xlsx'''
        games_file_path = os.path.join(_TMP, games_file_name)
        basket_data.to_excel(games_file_path)

        missing_games_file_name = f'''FlashScore_missing_games_{pd.Timestamp.today().strftime('%d%m%y_%H%M')}.xlsx'''
        missing_games_file_path = os.path.join(_TMP, missing_games_file_name)
        missing_data.to_excel(missing_games_file_path)

        logger.info(f'Files written to {games_file_path} and {missing_games_file_path}. Script complete')

    except Exception:
        raise Exception(f'The script {__name__} failed to complete')

    pass


if __name__ == '__main__':
    main()
