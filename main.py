"""
This is the main driver module that handles the interactions between the other modules
"""

import PySide6.QtWidgets as QtWidgets
import db_utils as db
from database_viewer_ui import database_viewer
from gather_data import get_json_data
from process_data import process
from style_sheet import set

DB_NAME = "form_entries.db"
TABLE_NAME = "entries"
TESTING = False


def main():  # comment to test workflow
    """The main function calls other functions and passes their return values to the next step"""
    json_object: dict[str, list[dict[str, str]]] = get_json_data()

    db_connection, db_cursor, table_name = db.set_up_database(
        DB_NAME, TABLE_NAME)

    process(json_object, db_cursor, table_name, TESTING)

    db.shutdown_database(db_connection)


if __name__ == "__main__":
    main()
    app = QtWidgets.QApplication([])
    app_palette = app.palette()
    app_paltete = set(app_palette)
    app.setPalette(app_palette)
    app.setStyle('Fusion')

    MainWindow = QtWidgets.QMainWindow()
    ui = database_viewer(MainWindow)
    MainWindow.show()
    print('Running UI')
    app.exec()
