"""
This module holds all of the interactions with the database
"""

import sqlite3


def set_up_database() -> sqlite3.Connection | sqlite3.Cursor | str:
    """This function sets up our database and then creates the table. The function
    returns the important connection and cursor objects for use throughout the program"""
    db_connection = None
    try:
        # initialize the database and its important connection/cursor objects
        db_name = 'form_entries.db'
        db_connection = sqlite3.connect(db_name)
        db_cursor = db_connection.cursor()
        print('Successfully connected to database')
        # create the table
        table_name = "entries"
        make_entry_table(db_cursor, db_connection, table_name)
        print('Successfully created all tables')
    except sqlite3.Error as db_error:
        print(f'A database error has occurred: {db_error}')
    finally:
        return db_connection, db_cursor, table_name


def make_entry_table(db_cursor: sqlite3.Cursor, db_connection: sqlite3.Connection, table_name: str) -> None:
    """This function creates the table if it doesn't exist yes and clears it of old data."""
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
    except sqlite3.Error as create_error:
        print(f'A database table creation error has occurred: {create_error}')


def insert_data(entry_lst: list, db_cursor: sqlite3.Cursor, table_name: str) -> None:
    """This function takes a list and a table name and inserts the data from the list into the table with the cursor"""
    prefix, firstName, lastName, title, orgName, email, orgWebsite, phoneNumber, courseProject, guestSpeaker, siteVisit, \
        jobShadow, internships, careerPanel, networkingEvent, summer2022, fall2022, spring2023, summer2023, otherTime, \
        namePermission = entry_lst
    try:
        db_cursor.execute(f'''INSERT INTO {table_name} (prefix, firstName, lastName, title, orgName, phoneNumber, email, \
            orgWebsite, courseProject, guestSpeaker, siteVisit, jobShadow, internships, careerPanel, networkingEvent, \
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

        print('All data succesfully inserted into table.')
    except sqlite3.Error as insert_error:
        print(f'A database insert error has occurred: {insert_error}')


def shutdown_database(db_connection: sqlite3.Connection) -> None:
    """This function actually populates the database tables and disconnects from the database"""
    db_connection.commit()
    db_connection.close()
