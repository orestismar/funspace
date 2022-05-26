"""

TODO
"""

import os
import pandas as pd

from directories import _TMP
from logs import get_stream_and_file_logger

logger = get_stream_and_file_logger(name=__name__)


def load_basketball_match_df(filename='FlashScore_data_201021.xlsx'):
    """
    TODO consider if we need to slim this down
    :return:
    """

    filepath = os.path.join(_TMP, filename)
    data = pd.read_excel(io=filepath,
                         engine='openpyxl')

    logger.info(f'Opened the file')

    pass


def test_load_basketball_match_df():
    load_basketball_match_df()

    pass