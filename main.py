from gather_data import get_json_data
from process_data import process
import db_utils as db


def main():
    json_object = get_json_data()
    db_connection, db_cursor, table_name = db.set_up_database()
    process(json_object, db_cursor, table_name)
    db.shut_down_data_base(db_connection)


if __name__ == "__main__":
    main()
