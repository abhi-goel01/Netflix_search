"""
Author = Abhishek Goel
Purpose = Execute SQL commands to interact with SQLITE database
"""
# This function creates a new database
def create_database(csr):

    main = """
    CREATE TABLE IF NOT EXISTS netflix_main(
     netflix_id INTEGER PRIMARY KEY,
     imdb_id TEXT,
     title TEXT,
     type TEXT,
     netflix_rating REAL,
     year_released INTEGER,
     imdb_id_searched TEXT);
    """
    csr.execute(main)

    extended = """
    CREATE TABLE IF NOT EXISTS netflix_extended(
     netflix_id INTEGER PRIMARY KEY,
     imdb_id TEXT,
     run_time TEXT,
     image TEXT,
     large_image TEXT,
     synopsis TEXT);
    """
    csr.execute(extended)

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
