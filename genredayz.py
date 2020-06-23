"""
Author: Abhishek Goel
Purpose: Create the genre reference and mapping table for day 0 load
"""

import sqlite3
import os
from sql_helper1 import *

data = []
unique_genre = []
count = 0

dbname = 'netflixdb.sqlite'
db_is_new = not os.path.exists(dbname)

if not db_is_new:
    # Connect to the SQLITE database
    conn = sqlite3.connect(dbname)
    csr = conn.cursor()
    # Create the genre tables
    create_genre_ref(csr)
    create_genre_title_map(csr)
    # Read the genre from all titles and move them into an array
    data = read_genre_data(csr)
    conn.close()

# De-duplicate the genres and insert them into an array
for i in data:
    count = count + 1
    str = i[2].lower().replace(" ", "").split(',')
    for k in str:
        if k in unique_genre: continue
        unique_genre.append(k)

# Write the genre reference table
conn = sqlite3.connect(dbname)
csr = conn.cursor()
update_genre_ref(csr,unique_genre)
conn.commit()
conn.close()

print('number of titles read:',count)
#print(unique_genre)
