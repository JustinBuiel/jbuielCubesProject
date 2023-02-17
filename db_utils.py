"""
Holds all of the interactions with the database
"""

import sqlite3


def set_up_database(db_name: str, table_name: str) -> sqlite3.Connection | sqlite3.Cursor | str:
    """Sets up our database and then creates the table. The names for the databse and table(s) are accepted as parameters.
    The function returns the important connection and cursor objects and table_name for use throughout the program."""
    db_connection = None
    try:
        # initialize the database and its important connection/cursor objects
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        print('Successfully connected to database')

        # create the table(s)
        _make_entry_table(db_connection, db_cursor, table_name)
        print('Successfully created all tables')
    except sqlite3.Error as connection_error:
        print(f'A database error has occurred: {connection_error}')
    finally:
        return db_connection, db_cursor, table_name


def _make_entry_table(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, table_name: str) -> None:
    """Creates the table if it doesn't exist yet and clears it of old data."""
    try:
        db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                             entryID INTEGER PRIMARY KEY,
                             prefix TEXT,
                             firstName TEXT,
                             lastName TEXT,
                             title TEXT,
                             orgName TEXT,
                             email TEXT,
                             orgWebsite TEXT,
                             phoneNumber TEXT,
                             courseProject TEXT,
                             guestSpeaker TEXT,
                             siteVisit TEXT,
                             jobShadow TEXT,
                             internships TEXT,
                             careerPanel TEXT,
                             networkingEvent TEXT,
                             summer2022 TEXT,
                             fall2022 TEXT,
                             spring2023 TEXT,
                             summer2023 TEXT,
                             otherTime TEXT,
                             namePermission TEXT);''')
        db_cursor.execute(f'''DELETE FROM {table_name}''')
        db_connection.commit()
    except sqlite3.Error as creation_error:
        print(f'A database table creation error occurred: {creation_error}')


def insert_data(entry_lst: list, db_cursor: sqlite3.Cursor, table_name: str) -> None:
    """Inserts the entry data from the list into the appropriate table"""
    prefix, firstName, lastName, title, orgName, email, orgWebsite, phoneNumber, courseProject, guestSpeaker, siteVisit, \
        jobShadow, internships, careerPanel, networkingEvent, summer2022, fall2022, spring2023, summer2023, otherTime, \
        namePermission = entry_lst
    try:
        db_cursor.execute(f'''INSERT INTO {table_name} (prefix, firstName, lastName, title, orgName, email, orgWebsite, \
            phoneNumber, courseProject, guestSpeaker, siteVisit, jobShadow, internships, careerPanel, networkingEvent, \
                summer2022, fall2022, spring2023, summer2023, otherTime, namePermission) \
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (prefix,
                           firstName,
                           lastName,
                           title,
                           orgName,
                           email,
                           orgWebsite,
                           phoneNumber,
                           courseProject,
                           guestSpeaker,
                           siteVisit,
                           jobShadow,
                           internships,
                           careerPanel,
                           networkingEvent,
                           summer2022,
                           fall2022,
                           spring2023,
                           summer2023,
                           otherTime,
                           namePermission))
    except sqlite3.Error as insert_error:
        print(f'A database insert error has occurred: {insert_error}')


def shutdown_database(db_connection: sqlite3.Connection) -> None:
    """Populates the database tables and disconnects from the database"""
    try:
        db_connection.commit()
        db_connection.close()
    except sqlite3.Error as shutdown_error:
        print(f'A database shutdown error has occurred: {shutdown_error}')


def get_minimal_data(db_cursor: sqlite3.Cursor) -> list:
    return_list = []
    try:
        response = db_cursor.execute(
            '''SELECT entryID, orgName, lastName, firstName FROM entries''')
    except sqlite3.Error as minimal_data_error:
        print(
            f'A database error while accessing minimal data has occurrred: {minimal_data_error}')
    for row in response:
        string = str(str(row[0]) + '. ' + row[1] + ': ' +
                     row[2] + ', ' + row[3])
        return_list.append(string)

    return return_list


def get_entries_dict(db_cursor: sqlite3.Cursor) -> dict:
    """get a dictionary of the entries and return it so the info page can be populated
    without accessing the database every time"""
    return_dict = {}
    try:
        response = db_cursor.execute('''SELECT * FROM entries''')
    except sqlite3.Error as get_entries_error:
        print(
            f'A database access error has occurred while getting entry data for dictionary storage: {get_entries_error}')

    for row in response:
        return_dict[int(row[0])] = labelled_info_dict(row[1:])

    return return_dict


def labelled_info_dict(res_tuple: tuple) -> dict:
    """Create the dictionary that each id gets mapped to"""
    return_dict = {}

    return_dict[' Prefix'] = res_tuple[0]
    return_dict[' First Name'] = res_tuple[1]
    return_dict[' Last Name'] = res_tuple[2]
    return_dict[' Title'] = res_tuple[3]
    return_dict[' Organization Name'] = res_tuple[4]
    return_dict[' Email'] = res_tuple[5]
    return_dict[' Organization Website'] = res_tuple[6]
    return_dict[' Phone Number'] = res_tuple[7]
    return_dict[' Course Project'] = res_tuple[8]
    return_dict[' Guest Speaker'] = res_tuple[9]
    return_dict[' Site Visit'] = res_tuple[10]
    return_dict[' Job Shadow'] = res_tuple[11]
    return_dict[' Internships'] = res_tuple[12]
    return_dict[' Career Panel'] = res_tuple[13]
    return_dict[' Networking Event'] = res_tuple[14]
    return_dict[' Summer 2022'] = res_tuple[15]
    return_dict[' Fall 2022'] = res_tuple[16]
    return_dict[' Spring 2023'] = res_tuple[17]
    return_dict[' Summer 2023'] = res_tuple[18]
    return_dict[' Other Timeframe'] = res_tuple[19]
    return_dict['Org Name Permission'] = res_tuple[20]

    return return_dict
