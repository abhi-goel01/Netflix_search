"""
Author: Abhishek Goel
Purpose: Execute multiple functions required for reading and writing netflix data
"""

# This functions checks the database to see if the title being loaded already exists
def check_if_exists(flixid):
        import sqlite3
        import os
        from sql_helper import check_database

        flag = None
        # Check if the DB already exists in the operating system
        dbname = 'netflixdb.sqlite'
        db_is_new = not os.path.exists(dbname)

        if not db_is_new:
            # Connect to the SQLITE database
            conn = sqlite3.connect(dbname)
            csr = conn.cursor()
            flag = check_database(csr, flixid)
        return flag
        conn.close()

# This function loads the data in SQLITE from the Python table structure
def execute_sql(table_titles):
    import sqlite3
    import os
    from sql_helper import create_database, update_database

    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()

    # Create a new database if none exists
    if db_is_new:
        print('creating a new database')
        create_database(csr)
        update_database(csr, table_titles)
    else:
        update_database(csr, table_titles)

    # commit the data and close SQL connection
    conn.commit()
    conn.close()

# This functions returns all those titles where imdbid is missing
def find_missing_imdbid(api_name):
    import sqlite3
    import os
    from sql_helper import find_missing_imdb, find_missing_imdb2

    # List of titles missing imdbID's
    missing_imdb = []
    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    if not db_is_new:
        # Connect to the SQLITE database
        conn = sqlite3.connect(dbname)
        csr = conn.cursor()
        if api_name == 'api1': data = find_missing_imdb(csr)
        elif api_name == 'api2': data = find_missing_imdb2(csr)
        if len(data)>0:
            missing_imdb = data
        else:
            missing_imdb = []
        return missing_imdb
    conn.close()

# This function loads the data in SQLITE from the Python table structure
def execute_sql2(missing_imdb_result):
    import sqlite3
    import os
    from sql_helper import update_database2

    # Check if the DB already exists in the operating system
    dbname = 'netflixdb.sqlite'
    db_is_new = not os.path.exists(dbname)

    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()

    # Create a new database if none exists
    if not db_is_new:
        update_database2(csr, missing_imdb_result)

    # commit the data and close SQL connection
    conn.commit()
    conn.close()
