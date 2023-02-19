import db_utils as db
from gather_data import get_json_data
from process_data import process
from database_viewer_ui import database_viewer
import sqlite3
import PySide6.QtWidgets as QtWidgets


def test_api_data_amount():
    # test 1 sprint 2
    json_test = get_json_data()
    lst_test = json_test['Entries']
    assert len(lst_test) >= 10


def test_entry_in_database():
    # test 2 sprint 2
    db_connection, db_cursor, raw_entries_dict = database_helper()

    response = db_cursor.execute('''SELECT * FROM testTable''')
    count = 1
    for row in response:
        entries_tuple = raw_entries_dict[count]
        assert entries_tuple == row
        count += 1
    db_connection.close()


def test_data_in_table():
    # test 3 sprint 3
    db_connection, db_cursor, raw_entries_dict = database_helper()

    db_cursor.execute('''SELECT * FROM testTable''')
    results = db_cursor.fetchall()
    if len(results) > 0:
        assert True
    else:
        assert False

    db.shutdown_database(db_connection)

    db_connection, db_cursor = database_unhelper()

    db_cursor.execute('''SELECT * FROM testTable''')
    results = db_cursor.fetchall()
    # no data inserted so there shouldn't be any responses
    if len(results) == 0:
        assert True
    else:
        assert False


def test_gui_info():
    # test 4 sprint 3
    QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = database_viewer(MainWindow)
    labelled_entries_dict = get_labelled_dict()
    ui.show_data(id=2, labelled_entries_dict=labelled_entries_dict)

    response = ui.rightLayout.itemAt(3).widget()
    assert response.text() == labelled_entries_dict[2][' First Name']

    response = ui.rightLayout.itemAt(5).widget()
    assert response.text() == labelled_entries_dict[2][' Last Name']

    response = ui.rightLayout.itemAt(11).widget()
    assert response.text() == labelled_entries_dict[2][' Email']

    response = ui.rightLayout.itemAt(13).widget()
    assert response.text() == labelled_entries_dict[2][' Organization Website']

    response = ui.rightLayout.itemAt(19).widget()
    if labelled_entries_dict[2][' Course Project'] == 'yes':
        assert response.isChecked() is True
    else:
        assert response.isChecked() is False

    response = ui.rightLayout.itemAt(20).widget()
    if labelled_entries_dict[2][' Guest Speaker'] == 'yes':
        assert response.isChecked() is True
    else:
        assert response.isChecked() is False

    response = ui.rightLayout.itemAt(23).widget()
    if labelled_entries_dict[2][' Internships'] == 'yes':
        assert response.isChecked() is True
    else:
        assert response.isChecked() is False

    response = ui.rightLayout.itemAt(30).widget()
    if labelled_entries_dict[2][' Summer 2023'] == 'yes':
        assert response.isChecked() is True
    else:
        assert response.isChecked() is False


def database_helper():
    json_test = get_json_data()
    db_connection, db_cursor, table_name = db.set_up_database(
        db_name="data_testing.db", table_name="testTable")
    raw_entries_dict = process(json_test, db_cursor, table_name, True)
    db_connection.commit()

    return db_connection, db_cursor, raw_entries_dict


def database_unhelper():
    db_connection, db_cursor, table_name = db.set_up_database(
        db_name="data_testing.db", table_name="testTable")
    db_connection.commit()

    return db_connection, db_cursor


def get_labelled_dict():
    try:
        db_connection = sqlite3.connect('form_entries.db')
        db_cursor = db_connection.cursor()
        labelled_entries_dict = db.get_entries_dict(db_cursor)
    except sqlite3.Error as db_connect_error:
        print(f'A gui database error has occurred: {db_connect_error}')
    return labelled_entries_dict
