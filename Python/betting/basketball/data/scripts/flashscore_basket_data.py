"""

Automate scrapping from Flash Score
"""

import os

import pandas as pd

from betting.basketball.data.utils import get_flashscore_basket_data
from directories import _TMP





# TODO - include this date in the logic - maybe read the last date from excel/database
last_cached_date = None


def main():
    try:
        basket_data = get_flashscore_basket_data()

        # TODO cache/save the latest date games so that we don't have to copy everything every time
        # TODO we also need a way to update the data set in this case

        # Write the data to an excel file
        file_name = f'''FlashScore_data_{pd.Timestamp.today().strftime('%d%m%y')}.xlsx'''
        file_path = os.path.join(_TMP, file_name)

        basket_data.to_excel(file_path)

        print(f'File written to {file_path}. Script complete')

    except Exception:
        raise Exception(f'The script {__name__} failed to complete')

    pass


if __name__ == '__main__':
    main()
