"""
SQlite database setup and examples

Date: 27/11/2022
"""

from logs import get_stream_and_file_logger
import sqlite3
from typing import Dict, Tuple, Union, List

logger = get_stream_and_file_logger(name=__name__)

data_path = "C:\\Data\\"


# Another way of generating databases using SQLite in Python is to create them in memory.
# This is a great way to generate databases that can be used for testing purposes, as they exist only in RAM.
# conn = sqlite3.connect(:memory:)
#

def create_connection(db_file) -> Union[sqlite3.Connection, None]:
    """ Create a database connection to the SQLite database specified by db_file
    :param db_file: database file path
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(f'{data_path}/{db_file}.db')
        logger.info(f"Successfully connected to {db_file}")
    except sqlite3.Error as e:
        logger.error(e)

    return conn


def create_new_table(conn, table_name: str, primary_key: Tuple[str, str], fields: Dict[str, str]) -> None:
    """
    Creates new sqlite table using this function
    :param conn: the connection to the database object
    :param table_name: <<
    :param primary_key: tuple containing the field and type of the primary key of the table
    :param fields: dict of fields in the table as keys and their type as values. Should not include the primary key
    :return: None

    cur.execute(
        "
           CREATE TABLE IF NOT EXISTS users (
           userid INT PRIMARY KEY,
           fname TEXT,
           lname TEXT,
           gender TEXT);
        ")

    """

    create_str = f"""CREATE TABLE IF NOT EXISTS {table_name}(\n{primary_key[0]} {primary_key[1].upper()} PRIMARY KEY """

    # Create string to use
    for field, sql_type in fields.items():
        create_str += f""",\n
           {field} {sql_type.upper()}"""

    create_str += ");"

    try:
        # A cursor object allows us to execute SQL queries against a database
        c = conn.cursor()
        c.execute(create_str)
        logger.info(f"Successfully created table {table_name}")
    except Exception as e:
        logger.exception(e)

    finally:

        conn.commit()

    pass


def insert_multiple_records(database: str, table: str, records: List) -> bool:
    """
    Inserts the given records to the designated table in the specified db.
    :param database: db to extend
    :param table: db table to insert to
    :param records: data to insert
    :return: True if successfully inserted, False otherwise
    """

    successful = False
    conn = None

    try:
        conn = sqlite3.connect(f'{database}.db')
        cursor = conn.cursor()
        logger.info(f"Connected to SQLite {database}")

        tb_fields = get_sqlite_table_fields(database=database, table=table)
        val_str = ['?' for i in range(len(tb_fields))]

        sqlite_insert_query = f"""INSERT INTO {table}
                                {tuple(tb_fields)} 
                                VALUES {tuple(val_str)};"""

        cursor.executemany(sqlite_insert_query, records)
        conn.commit()
        logger.info("Total", cursor.rowcount, "Records inserted successfully into SqliteDb_developers table")
        conn.commit()
        cursor.close()
        successful = True

    except sqlite3.Error as error:
        logger.error("Failed to insert multiple records into sqlite table", error)
    finally:
        if conn:
            conn.close()
            logger.info("The SQLite connection is closed")

    return successful


def get_sqlite_table_fields(database: str, table: str) -> List[str]:
    """
    :return: the list of fields in a table
    """
    connection = sqlite3.connect(f'{database}.db')
    cursor = connection.execute(f'SELECT * FROM {table}')

    names = [description[0] for description in cursor.description]
    return names

