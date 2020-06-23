"""
Author: Abhishek Goel
Purpose: Execute multiple functions required for reading and writing imdb data
"""

# This functions returns all those titles where imdb data has not been added
def find_missing_imdbdata():
    import sqlite3
    import os
    from sql_helper import find_missing_imdbdata

    # List of titles missing imdbID's
    missing_imdbdata = []
    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    if not db_is_new:
        # Connect to the SQLITE database
        conn = sqlite3.connect(dbname)
        csr = conn.cursor()
        data = find_missing_imdbdata(csr)
        if len(data)>0:
            missing_imdbdata = data
        else:
            missing_imdbdata = []
        return missing_imdbdata
    conn.close()

# This function loads the data in SQLITE from the Python table structure
def execute_sql3(table_imdb_found):
    import sqlite3
    import os
    from sql_helper import update_database3

    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()

    # Create a new database if none exists
    if not db_is_new:
        update_database3(csr, table_imdb_found)

    # commit the data and close SQL connection
    conn.commit()
    conn.close()

# This function loads the data in SQLITE from the Python table structure
def execute_sql4(table_imdb_not_found):
    import sqlite3
    import os
    from sql_helper import update_database4

    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()

    # Create a new database if none exists
    if not db_is_new:
        update_database4(csr, table_imdb_not_found)

    # commit the data and close SQL connection
    conn.commit()
    conn.close()
