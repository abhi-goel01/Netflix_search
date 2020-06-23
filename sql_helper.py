"""
Author = Abhishek Goel
Purpose = Execute SQL commands to interact with SQLITE database
"""
# This function creates a new database
def create_database(csr):

    netflix_main = """
    CREATE TABLE IF NOT EXISTS netflix_main(
     netflix_id INTEGER PRIMARY KEY,
     imdb_id TEXT,
     title TEXT,
     type TEXT,
     netflix_rating REAL,
     year_released INTEGER,
     imdb_id_searched TEXT);
    """
    csr.execute(netflix_main)

    netflix_extended = """
    CREATE TABLE IF NOT EXISTS netflix_extended(
     netflix_id INTEGER PRIMARY KEY,
     imdb_id TEXT,
     run_time TEXT,
     image TEXT,
     large_image TEXT,
     synopsis TEXT);
    """
    csr.execute(netflix_extended)

    imdb_main = """
    CREATE TABLE IF NOT EXISTS imdb_main(
     imdb_id TEXT PRIMARY KEY,
     imdb_data_found TEXT,
     title TEXT,
     year_released INTEGER,
     rated TEXT,
     genre TEXT,
     language TEXT,
     country TEXT,
     type TEXT,
     imdb_rating REAL,
     imdb_votes TEXT);
    """
    csr.execute(imdb_main)

    imdb_extended = """
    CREATE TABLE IF NOT EXISTS imdb_extended(
     imdb_id TEXT PRIMARY KEY,
     imdb_data_found TEXT,
     date_released INTEGER,
     run_time TEXT,
     director TEXT,
     writers TEXT,
     actors TEXT,
     plot TEXT,
     awards TEXT,
     poster TEXT,
     dvd_date TEXT,
     box_office TEXT,
     production TEXT);
    """
    csr.execute(imdb_extended)

# This function updates the tables in database
def update_database(csr, table_titles):
    main = """ INSERT INTO netflix_main VALUES (:netflixid, :imdbid, :title, :type, :rating, :released, :searched) """
    csr.executemany(main, table_titles)

    extended = """ INSERT INTO netflix_extended VALUES (:netflixid, :imdbid, :runtime, :image, :largeimage, :synopsis) """
    csr.executemany(extended, table_titles)

# This function updates the tables in database
def update_database2(csr, missing_imdb_result):
    for i in missing_imdb_result:
        flixid = i[0]
        imdbid = i[1]
        flag = i[2]
        csr.execute('UPDATE netflix_main SET imdb_id = ?, imdb_id_searched = ? WHERE netflix_id = ?',(imdbid,flag,flixid))
        if flag == 'api1-found' or flag == 'api2-found':
            csr.execute('UPDATE netflix_extended SET imdb_id = ? WHERE netflix_id = ?',(imdbid,flixid))

# This function updates the tables in database
def update_database3(csr, table_imdb_found):
    main = """ INSERT INTO imdb_main VALUES (:imdbID, :imdb_data_found, :Title, :Year, :Rated, :Genre, :Language, :Country, :Type, :imdbRating, :imdbVotes) """
    csr.executemany(main, table_imdb_found)

    extended = """ INSERT INTO imdb_extended VALUES (:imdbID, :imdb_data_found, :Released, :Runtime, :Director, :Writer, :Actors, :Plot, :Awards, :Poster, :DVD, :BoxOffice, :Production) """
    csr.executemany(extended, table_imdb_found)

# This function updates the tables in database
def update_database4(csr, table_imdb_not_found):
    main = """ INSERT INTO imdb_main(imdb_id, imdb_data_found) VALUES (:imdbID, :imdb_data_found) """
    csr.executemany(main, table_imdb_not_found)

    extended = """ INSERT INTO imdb_extended(imdb_id, imdb_data_found) VALUES (:imdbID, :imdb_data_found) """
    csr.executemany(extended, table_imdb_not_found)

# This function checks the database to see if a movie already exists
def check_database(csr, flixid):
    csr.execute("SELECT netflix_id FROM netflix_main WHERE netflix_id = ?",(flixid,))
    try:
        data = csr.fetchone()[0]
        #print('Skipping Netflix ID',flixid,'as it already exists in the DB')
        flag = 'Exists'
    except:
        flag = 'does not exist'
    return flag

# This function checks the database to see which titles do not have an imdbID
def find_missing_imdb(csr):
    csr.execute("SELECT title, netflix_id FROM netflix_main WHERE imdb_id_searched = 'no'")
    try:
        data = csr.fetchall()
    except:
        data = []
    # data contains matched rows as a list of tuple
    return data

# This function checks the database to see for which titles IMDB API 1 could not find an imdbID
def find_missing_imdb2(csr):
    csr.execute("SELECT title, netflix_id FROM netflix_main WHERE imdb_id_searched = 'api1-not found'")
    try:
        data = csr.fetchall()
    except:
        data = []
    # data contains matched rows as a list of tuple
    return data

# This function checks the database to see which titles do not have an imdb data
def find_missing_imdbdata(csr):
    qry = """
    SELECT a.imdb_id FROM netflix_main a LEFT JOIN imdb_main b ON a.imdb_id = b.imdb_id
    WHERE b.imdb_id IS NULL AND a.imdb_id_searched IN ('n/a','api1-found','api2-found')
    """
    csr.execute(qry)
    try:
        data = csr.fetchall()
    except:
        data = []
    # data contains matched rows as a list of tuple
    return data
