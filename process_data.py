"""
This module holds the functions used to process the json data taken from the wufoo API
"""

import sqlite3
import db_utils as db


def process(json_object: dict, db_cursor: sqlite3.Cursor, table_name: str, testing: bool) -> None:  # noqa: C901
    """This function loops through the entries returned by the API and gathers the data into a
    neat format for the database insertion"""
    lst = json_object['Entries']
    entry_list = []
    testing_dict = {}
    count = 1
    for entry in lst:

        info_checks(entry['Field1'], entry_list)
        entry_list.append(entry['Field2'])
        entry_list.append(entry['Field3'])
        entry_list.append(entry['Field4'])
        entry_list.append(entry['Field5'])
        info_checks(entry['Field6'], entry_list)
        info_checks(entry['Field7'], entry_list)

        if entry['Field9'] != '':
            entry_list.append(str(entry['Field9'][:3] + '-' +
                                  entry['Field9'][3:6] + '-' + entry['Field9'][6:]))
        else:
            entry_list.append(None)

        collab_checks(entry['Field11'], entry_list)
        collab_checks(entry['Field12'], entry_list)
        collab_checks(entry['Field13'], entry_list)
        collab_checks(entry['Field14'], entry_list)
        collab_checks(entry['Field15'], entry_list)
        collab_checks(entry['Field16'], entry_list)
        collab_checks(entry['Field17'], entry_list)

        collab_checks(entry['Field111'], entry_list)
        collab_checks(entry['Field112'], entry_list)
        collab_checks(entry['Field113'], entry_list)
        collab_checks(entry['Field114'], entry_list)
        collab_checks(entry['Field115'], entry_list)

        entry_list.append(entry['Field211'])

        db.insert_data(entry_list, db_cursor, table_name)

        if testing:
            entry_list.insert(0, count)
            entries_tuple: tuple = tuple(entry_list)
            testing_dict[count] = entries_tuple
            count += 1

        entry_list.clear()

    print('All data succesfully inserted into tables.')

    if testing:
        return testing_dict


def collab_checks(answer: str, entry_list: list) -> None:
    """This function takes the collaboration and timeframe choice fields and either passes the value or None (null)"""
    if answer != '':
        entry_list.append('yes')
    else:
        entry_list.append(None)


def info_checks(answer: str, entry_list: list) -> None:
    """This function takes the non-required fields and either passes the value or None (null)"""
    if answer != '':
        entry_list.append(answer)
    else:
        entry_list.append(None)
