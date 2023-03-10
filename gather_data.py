"""
Gather entry data from the form's backend
"""

import sys
from secrets import wufoo_key  # type: ignore reportShadowedImport
import requests
from requests.auth import HTTPBasicAuth
import db_utils as db
from process_data import process

TABLE_NAMES = ("entries", "user_information", "claimed_projects")
DB_NAME = "form_entries.db"
ENTRY_TABLE, USER_TABLE, CLAIM_TABLE = TABLE_NAMES

WUFOO_KEY: str = wufoo_key
URL = "https://justinb.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json"
TESTING = False


def update_data() -> None:  # comment to test workflow
    """The main function calls other functions and passes their return values to the next step"""
    json_object: dict[str, list[dict[str, str]]] = get_json_data()

    db_connection, db_cursor = db.set_up_database(
        DB_NAME, TABLE_NAMES)

    process(json_object, db_cursor, ENTRY_TABLE, TESTING)

    db.shutdown_database(db_connection)


def get_json_data() -> dict[str, list[dict[str, str]]]:
    """Accesses the JSON data from the form using httpbasicauth and the API key"""
    response = requests.get(URL, auth=HTTPBasicAuth(WUFOO_KEY, 'pass'))

    # No data retrieved, terminate program execution
    if response.status_code != 200:
        print(
            f'Failed to get data, response from website: {response.status_code} with error: {response.reason}')
        sys.exit(-1)

    json_object: dict = response.json()
    print('Data gathered from api')
    return json_object
