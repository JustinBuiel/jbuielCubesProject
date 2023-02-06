"""
This is the main driver module that handles the interactions between the other modules
"""

import db_utils as db
from gather_data import get_json_data
from process_data import process


def main():
    """The main function calls other functions and passes their return values to the next step"""
    json_object: dict = get_json_data()
    db_connection, db_cursor, table_name = db.set_up_database()
    process(json_object, db_cursor, table_name, False)
    db.shutdown_database(db_connection)


if __name__ == "__main__":
    main()
