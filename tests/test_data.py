from db_utils import set_up_database
from gather_data import get_json_data
from process_data import process


def test_data_amount():
    global json_test
    json_test = get_json_data()
    lst_test = json_test['Entries']
    assert len(lst_test) >= 10


def test_database():
    # create database and table, get data and insert into table
    db_connection, db_cursor, table_name = set_up_database(
        db_name="data_testing.db", table_name="testTable")
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
