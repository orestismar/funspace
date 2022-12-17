"""

Test suite for data_access.py
"""
import pytest
import os
import data_access
import sqlite3


@pytest.mark.parametrize('file', ['basketball', 'football'])
def test_create_connection(file):
    db_path = data_access.data_path
    test_conn = data_access.create_connection(db_file=file)
    db_filepath = os.path.join(db_path, f'{file}.db').rstrip()
    assert os.path.exists(db_filepath)
    assert isinstance(test_conn, sqlite3.Connection)

