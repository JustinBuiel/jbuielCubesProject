"""
Holds all of the interactions with the database
"""

import sqlite3


def set_up_database(db_name, table_name) -> sqlite3.Connection | sqlite3.Cursor | str:
    """Sets up our database and then creates the table. The names for the databse and table(s) are accepted as parameters.
    The function returns the important connection and cursor objects and table_name for use throughout the program."""
    db_connection = None
    try:
        # initialize the database and its important connection/cursor objects
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        print('Successfully connected to database')

        # create the table(s)
        make_entry_table(db_connection, db_cursor, table_name[0])
        print('Successfully created all tables')
    except sqlite3.Error as connection_error:
        print(f'A database error has occurred: {connection_error}')
    finally:
        return db_connection, db_cursor, table_name


def make_entry_table(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, table_name: str) -> None:
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
