import db_utils as db
from gather_data import get_json_data
from process_data import process
from database_viewer_ui import database_viewer
import PySide6.QtWidgets as QtWidgets

DB_NAME = "data_testing.db"
TABLE_NAME = "test_table"
IDS_TO_TEST = [5, 1, 3, 12, 1]
JSON_TEST = get_json_data()


def test_api_data_amount():
    # test 1 sprint 2
    lst_test = JSON_TEST['Entries']
    assert len(lst_test) >= 10


def test_entry_in_database():
    # test 2 sprint 2
    DB_CONNECTION, DB_CURSOR = db.set_up_database(DB_NAME, TABLE_NAME)
    RAW_ENTRIES = process(JSON_TEST, DB_CURSOR, TABLE_NAME, True)
    response = DB_CURSOR.execute(f'''SELECT * FROM {TABLE_NAME}''')
    counter = 1
    for row in response:
        assert RAW_ENTRIES[counter] == row
        counter += 1

    db.shutdown_database(DB_CONNECTION)


def test_data_in_table():
    # test 3 sprint 3
    DB_CONNECTION, DB_CURSOR = db.set_up_database(DB_NAME, TABLE_NAME)
    RAW_ENTRIES = process(JSON_TEST, DB_CURSOR, TABLE_NAME, True)

    DB_CURSOR.execute(f'''SELECT * FROM {TABLE_NAME}''')
    results = DB_CURSOR.fetchall()
    if len(results) > 0:
        assert True
        assert len(RAW_ENTRIES) == len(results)
    else:
        assert False

    db.shutdown_database(DB_CONNECTION)

    DB_CONNECTION, DB_CURSOR = db.set_up_database(DB_NAME, TABLE_NAME)

    DB_CURSOR.execute(f'''SELECT * FROM {TABLE_NAME}''')
    results = DB_CURSOR.fetchall()
    # no data inserted so there shouldn't be any responses
    if len(results) == 0:
        assert True
    else:
        assert False

    db.shutdown_database(DB_CONNECTION)


def test_gui_info():
    # test 4 sprint 3
    DB_CONNECTION, DB_CURSOR = db.set_up_database(DB_NAME, TABLE_NAME)
    process(JSON_TEST, DB_CURSOR, TABLE_NAME, False)
    tagged_entries = db.get_tagged_dict(DB_CURSOR, TABLE_NAME)
    db.shutdown_database(DB_CONNECTION)

    QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    ui = database_viewer(main_window, DB_NAME, TABLE_NAME)

    for ID in IDS_TO_TEST:
        ui.show_entry_data(ID)

        response = ui.right_layout.itemAt(3).widget()
        assert response.text() == tagged_entries[ID]['First Name']

        response = ui.right_layout.itemAt(5).widget()
        assert response.text() == tagged_entries[ID]['Last Name']

        response = ui.right_layout.itemAt(12).widget()
        assert response.text() == tagged_entries[ID]['Email']

        response = ui.right_layout.itemAt(14).widget()
        assert response.text(
        ) == tagged_entries[ID]['Organization Website']

        response = ui.right_layout.itemAt(19).widget()
        if tagged_entries[ID]['Course Project'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(20).widget()
        if tagged_entries[ID]['Guest Speaker'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(23).widget()
        if tagged_entries[ID]['Internships'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(30).widget()
        if tagged_entries[ID]['Summer 2023'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False
