"""
Functions used to process the json data taken from the wufoo API
"""

import sqlite3
from datetime import datetime
import db_utils as db


def process(json_object: dict, db_cursor: sqlite3.Cursor, table_name: str, testing: bool) -> None:
    """Loops through the entries returned by the API and gathers the data into a
    neat format for the database insertion"""
    global time
    time = datetime.now().strftime('%Y%m%d-%H%M%S')

    lst = json_object['Entries']
    entry_list = []
    testing_dict = {}
    count = 1

    text_file_creation(lst)
    print('Data written to file')

    for entry in lst:
        # personal information
        info_checks(entry['Field1'], entry_list)
        entry_list.append(entry['Field2'])
        entry_list.append(entry['Field3'])
        entry_list.append(entry['Field4'])
        entry_list.append(entry['Field5'])
        info_checks(entry['Field6'], entry_list)
        info_checks(entry['Field7'], entry_list)

        # format phone number
        if entry['Field9'] != '':
            entry_list.append(str(entry['Field9'][:3] + '-' +
                                  entry['Field9'][3:6] + '-' + entry['Field9'][6:]))
        else:
            entry_list.append(None)

        # what collaborations they are interested in
        collab_checks(entry['Field11'], entry_list)
        collab_checks(entry['Field12'], entry_list)
        collab_checks(entry['Field13'], entry_list)
        collab_checks(entry['Field14'], entry_list)
        collab_checks(entry['Field15'], entry_list)
        collab_checks(entry['Field16'], entry_list)
        collab_checks(entry['Field17'], entry_list)

        # what timeframe they are interested in
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
    """Takes the collaboration and timeframe choice fields and either passes yes or None (null)"""
    if answer != '':
        entry_list.append('yes')
    else:
        entry_list.append(None)


def info_checks(answer: str, entry_list: list) -> None:
    """Takes the non-required fields and either passes the value or None (null)"""
    if answer != '':
        entry_list.append(answer)
    else:
        entry_list.append(None)


def write_data_to_file(str: str, fileIO) -> None:
    """Takes a string from text_file_creation and writes to the file"""
    if str == '':
        return
    fileIO.write(str + '\n')


def text_file_creation(lst: list) -> None:
    """Takes the list of entries directly and provides a format to write to the file"""
    entries = len(lst)
    count = 0
    file_name = "form_entries.txt"

    with open(file_name, 'w') as fileIO:
        for entry in lst:
            count += 1
            for k, v in entry.items():
                write_data_to_file(f"{k}: {v}", fileIO)
            if entries != count:
                write_data_to_file('\n', fileIO)
                write_data_to_file('~~'*24, fileIO)
                write_data_to_file('\n', fileIO)
