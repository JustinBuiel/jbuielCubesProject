"""
Functions used to process the json data taken from the wufoo API
"""

import sqlite3
import db_utils as db


def process(json_object: dict[str, list[dict[str, str]]], db_cursor: sqlite3.Cursor, table_name: str, testing: bool) -> None:
    """Loops through the entries returned by the API and gathers the data into a
    neat format for the database insertion"""

    list_of_entries = json_object['Entries']
    individual_entry_list = []
    testing_dict = {}
    testing_counter = 1

    _text_file_creation(list_of_entries)
    print('Data written to file')

    for entry in list_of_entries:
        # personal information
        _non_required_check(entry['Field1'], individual_entry_list)
        individual_entry_list.append(entry['Field2'])
        individual_entry_list.append(entry['Field3'])
        individual_entry_list.append(entry['Field4'])
        individual_entry_list.append(entry['Field5'])
        _non_required_check(entry['Field6'], individual_entry_list)
        _non_required_check(entry['Field7'], individual_entry_list)

        # format phone number
        if entry['Field9'] != '':
            individual_entry_list.append(str(entry['Field9'][:3] + '-' +
                                             entry['Field9'][3:6] + '-' + entry['Field9'][6:]))
        else:
            individual_entry_list.append(None)

        # what collaborations they are interested in
        _check_box_check(entry['Field11'], individual_entry_list)
        _check_box_check(entry['Field12'], individual_entry_list)
        _check_box_check(entry['Field13'], individual_entry_list)
        _check_box_check(entry['Field14'], individual_entry_list)
        _check_box_check(entry['Field15'], individual_entry_list)
        _check_box_check(entry['Field16'], individual_entry_list)
        _check_box_check(entry['Field17'], individual_entry_list)

        # what timeframe they are interested in
        _check_box_check(entry['Field111'], individual_entry_list)
        _check_box_check(entry['Field112'], individual_entry_list)
        _check_box_check(entry['Field113'], individual_entry_list)
        _check_box_check(entry['Field114'], individual_entry_list)
        _check_box_check(entry['Field115'], individual_entry_list)

        individual_entry_list.append(entry['Field211'])

        db.insert_data(individual_entry_list, db_cursor, table_name)

        if testing:
            individual_entry_list.insert(0, testing_counter)
            testing_dict[testing_counter] = tuple(individual_entry_list)
            testing_counter += 1

        individual_entry_list.clear()

    print('All data succesfully inserted into tables.')

    if testing:
        return testing_dict


def _non_required_check(answer: str, individual_entry_list: list) -> None:
    """Takes the non-required fields and either passes the value or None (null)"""
    if answer != '':
        individual_entry_list.append(answer)
    else:
        individual_entry_list.append(None)


def _check_box_check(answer: str, individual_entry_list: list) -> None:
    """Takes the collaboration and timeframe choice fields and either passes yes or None (null)"""
    if answer != '':
        individual_entry_list.append('yes')
    else:
        individual_entry_list.append(None)


def _write_data_to_file(str: str, fileIO) -> None:
    """Takes a string from text_file_creation and writes to the file"""
    if str == '':
        return
    fileIO.write(str + '\n')


def _text_file_creation(list_of_entries: list) -> None:
    """Takes the list of entries directly and provides a format to write to the file"""
    number_of_entries = len(list_of_entries)
    writing_counter = 0
    file_name = "form_entries.txt"

    with open(file_name, 'w') as fileIO:
        for entry in list_of_entries:
            writing_counter += 1
            for k, v in entry.items():
                _write_data_to_file(f"{k}: {v}", fileIO)
            if number_of_entries != writing_counter:
                _write_data_to_file('\n', fileIO)
                _write_data_to_file('~~'*24, fileIO)
                _write_data_to_file('\n', fileIO)
