"""
This is the main driver module that handles the interactions between the other modules
"""

import sys
import PySide6.QtWidgets as QtWidgets
import db_utils as db
import gui
from gather_data import get_json_data
from process_data import process


def main():  # comment to test workflow
    """The main function calls other functions and passes their return values to the next step"""
    json_object: dict = get_json_data()

    db_connection, db_cursor, table_name = db.set_up_database(
        db_name="form_entries.db", table_name="entries")
    process(json_object, db_cursor, table_name, False)

    db.shutdown_database(db_connection)


if __name__ == "__main__":
    # main()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui.list_of_btns(MainWindow)
    MainWindow.show()
    app.exec()
