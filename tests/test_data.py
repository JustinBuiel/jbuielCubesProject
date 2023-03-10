import db_utils as db
from gather_data import get_json_data, update_data
from process_data import process
from database_viewer_ui import database_viewer
import PySide6.QtWidgets as QtWidgets

DB_NAME = "data_testing.db"
TABLE_NAMES = ("test_entry_table", "test_user_table", "test_claim_table")
ENTRY_TABLE, USER_TABLE, CLAIM_TABLE = TABLE_NAMES
IDS_TO_TEST = [5, 1, 3, 12, 1]
JSON_TEST = get_json_data()


def test_api_data_amount():
    # test 1 sprint 2
    lst_test = JSON_TEST['Entries']
    assert len(lst_test) >= 10


def test_entry_in_database():
    # test 2 sprint 2
    db_connection, db_cursor = db.set_up_database(DB_NAME, TABLE_NAMES)
    raw_entries: dict[str, str] = process(
        JSON_TEST, db_cursor, ENTRY_TABLE, True)
    response = db_cursor.execute(f'''SELECT * FROM {ENTRY_TABLE}''')
    counter = 1
    for row in response:
        assert raw_entries[counter] == row
        counter += 1

    db.shutdown_database(db_connection)


def test_data_in_table():
    # test 3 sprint 3
    db_connection, db_cursor = db.set_up_database(DB_NAME, TABLE_NAMES)
    raw_entries = process(JSON_TEST, db_cursor, ENTRY_TABLE, True)

    db_cursor.execute(f'''SELECT * FROM {ENTRY_TABLE}''')
    results = db_cursor.fetchall()
    if len(results) > 0:
        assert True
        assert len(raw_entries) == len(results)
    else:
        assert False

    db.shutdown_database(db_connection)

    db_connection, db_cursor = db.set_up_database(DB_NAME, TABLE_NAMES)

    db_cursor.execute(f'''SELECT * FROM {ENTRY_TABLE}''')
    results = db_cursor.fetchall()
    # no data inserted so there shouldn't be any responses
    if len(results) == 0:
        assert True
    else:
        assert False

    db.shutdown_database(db_connection)


def test_gui_info():
    # test 4 sprint 3
    db_connection, db_cursor = db.set_up_database(DB_NAME, TABLE_NAMES)
    process(JSON_TEST, db_cursor, ENTRY_TABLE, False)
    tagged_entries = db.get_tagged_dict(db_cursor, ENTRY_TABLE)
    db.shutdown_database(db_connection)

    QtWidgets.QApplication([])
    update_data
    ui = database_viewer(DB_NAME, ENTRY_TABLE)

    for id in IDS_TO_TEST:
        ui.show_entry_data(id)

        response = ui.right_layout.itemAt(3).widget()
        assert response.text() == tagged_entries[id]['First Name']

        response = ui.right_layout.itemAt(5).widget()
        assert response.text() == tagged_entries[id]['Last Name']

        response = ui.right_layout.itemAt(12).widget()
        assert response.text() == tagged_entries[id]['Email']

        response = ui.right_layout.itemAt(14).widget()
        assert response.text(
        ) == tagged_entries[id]['Organization Website']

        response = ui.right_layout.itemAt(19).widget()
        if tagged_entries[id]['Course Project'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(20).widget()
        if tagged_entries[id]['Guest Speaker'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(23).widget()
        if tagged_entries[id]['Internships'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False

        response = ui.right_layout.itemAt(30).widget()
        if tagged_entries[id]['Summer 2023'] == 'yes':
            assert response.isChecked() is True
        else:
            assert response.isChecked() is False
