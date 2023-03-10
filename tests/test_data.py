import sqlite3
import db_utils as db
from gather_data import get_json_data, update_data
from process_data import process
from database_viewer_ui import database_viewer
from claim_window_ui import claim_window
# from update_or_show_ui import update_or_show
import PySide6.QtWidgets as QtWidgets

QtWidgets.QApplication([])

DB_NAME = "data_testing.db"
TABLE_NAMES = ("test_entry_table", "test_user_table", "test_claim_table")
ENTRY_TABLE, USER_TABLE, CLAIM_TABLE = TABLE_NAMES
IDS_TO_TEST = [5, 1, 3, 12, 1]
JSON_TEST = get_json_data()
USER_INFO = ("justin", "buiel", "student", "jbuiel@bridgew.edu", "comp sci")


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

    ui = database_viewer(DB_NAME, TABLE_NAMES)

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


def test_user_creation():
    db_connection, db_cursor = db.set_up_database(DB_NAME, TABLE_NAMES)
    db.create_user(DB_NAME, USER_TABLE, USER_INFO)
    db_cursor.execute(
        f'''SELECT * FROM {USER_TABLE} WHERE email like \'{USER_INFO[3]}\' ''')
    response = db_cursor.fetchall()
    db.shutdown_database(db_connection)

    assert response[0][1:] == USER_INFO


def test_user_auto_fill():
    db_connection = sqlite3.connect(DB_NAME)
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        f'''SELECT * FROM {USER_TABLE} WHERE email like \'{USER_INFO[3]}\' ''')
    response = db_cursor.fetchall()
    response = response[0][1:]
    claiming_window = claim_window(1, DB_NAME, TABLE_NAMES)
    claiming_window.email.setText(USER_INFO[3])
    claiming_window.check_for_user()

    assert claiming_window.first_name.text() == USER_INFO[0]
    assert claiming_window.last_name.text() == USER_INFO[1]
    assert claiming_window.title.text() == USER_INFO[2]
    assert claiming_window.email.text() == USER_INFO[3]
    assert claiming_window.dept.text() == USER_INFO[4]

    claiming_window.claim_handler()


def test_claim_process():
    db_connection = sqlite3.connect(DB_NAME)
    db_cursor = db_connection.cursor()
    process(JSON_TEST, db_cursor, ENTRY_TABLE, False)
    db.shutdown_database(db_connection)
    
    ui = database_viewer(DB_NAME, TABLE_NAMES)

    # project is claimed and cannot be claimed by new person as indicated by text and disabled
    assert ui.claim_button.isEnabled() is False
    assert ui.claim_button.text() == "Project Claimed by Above Faculty Member"
