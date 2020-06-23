"""
Author = Abhishek Goel
Purpose = Execute SQL commands to interact with SQLITE database
"""
# This function creates a new database
def create_genre_ref(csr):

    genre = """
    CREATE TABLE IF NOT EXISTS genre_ref(
     genre_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
     genre_name TEXT);
    """
    csr.execute(genre)

def create_genre_title_map(csr):

    genre_title_map = """
    CREATE TABLE IF NOT EXISTS genre_title_map(
     netflix_id INTEGER,
     imdb_id TEXT,
     genre_id INTEGER,
     PRIMARY KEY(netflix_id,genre_id));
    """
    csr.execute(genre_title_map)

def read_genre_data(csr):
    qry = """
    SELECT a.netflix_id, b.imdb_id, b.genre
    FROM netflix_main a INNER JOIN imdb_main b ON a.imdb_id = b.imdb_id
    WHERE b.imdb_data_found = 'yes' AND b.genre != 'N/A'
    """
    csr.execute(qry)
    try:
        data = csr.fetchall()
    except:
        data = []
    # data contains matched rows as a list of tuple
    return data

def update_genre_ref(csr, unique_genre):
    for genre in unique_genre:
        csr.execute('INSERT OR IGNORE INTO genre_ref(genre_name) VALUES(?)',(genre,))
