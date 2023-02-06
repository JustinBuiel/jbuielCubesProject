from gather_data import get_json_data
from db_utils import make_entry_table
from process_data import process
import sqlite3


def test_data_amount():
    global json_test
    json_test = get_json_data()
    lst_test = json_test['Entries']
    assert len(lst_test) == 2


def test_database():
    # create database and table, get data and insert into table
    db_connection, db_cursor, table_name = set_up_database()
    make_entry_table(db_connection, db_cursor, table_name)
    entries_dict = process(json_test, db_cursor, table_name, True)
    db_connection.commit()

    # get database data
    response = db_cursor.execute('''SELECT * FROM testTable''')
    count = 1
    for row in response:
        entries_tuple = entries_dict[count]
        assert entries_tuple == row
        count += 1
    db_connection.close()


def set_up_database() -> sqlite3.Connection | sqlite3.Cursor | str:
    """This function sets up our database and then creates the table. The function
    returns the important connection and cursor objects for use throughout the program"""
    db_connection = None
    try:
        # initialize the database and its important connection/cursor objects
        db_name = 'data_testing.db'
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        table_name = "testTable"
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    finally:
        return db_connection, db_cursor, table_name
