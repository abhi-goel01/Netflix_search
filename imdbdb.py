"""
Author: Abhishek Goel
Purpose: Read imdb data and load into SQLITE database
"""

import requests
import json
from imdbfunc import *

# Program variables
counter = 0
write_after = 50
found_by_api = 0
not_found_by_api = 0
imdb_dict = {}
table_imdb_found = []
table_imdb_not_found = []
missing_imdbdata = []
search_count_all = 0
search_count_input = 0
search_limit = 0
input_by_user_flag = 'no'

# Find out how many netflix IDs need data from imdb
missing_imdbdata = find_missing_imdbdata()
search_count_all = len(missing_imdbdata)
print('length: ', search_count_all)

# If there are no imdb IDs with missing imdb data then quit
if search_count_all < 1:
    print('No imdb IDs with missing IMDB data, quitting . . .')
    quit()

# imdb API to retrieve content
# Make a dummy call to see how many calls are remaining
url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
querystring = {"i":"imdb id","r":"json"}
headers = {
    'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
    'x-rapidapi-key': "4f3c8910e1msh805be8dd48010a8p1b15fbjsn906cc77a3e30"
    }

# Make one dummy call to find out the API calls remaining
querystring['i'] = 'tt4154796'
response = requests.request("GET", url, headers=headers, params=querystring)
api_limit = int(response.headers['x-ratelimit-requests-limit'])
gas = int(response.headers['x-ratelimit-requests-remaining'])

# See if we have sufficient calls remaining from our quota to process this request, keeping a buffer of 20 calls
if (gas-search_count_all) < 800:
    print("\033[91m{}\033[00m".format('Not enough API balance remaining to look for all missing imdb data . . .'))
    print('API daily limit:',api_limit)
    print('API calls remaining for today:',gas)
    print('API calls needed:',search_count_all)
    print('Buffer kept:','20')
    while True:
        items_to_search = input('Enter the number of imdb IDs you want to search or hit enter to quit: ')
        try:
            if len(items_to_search) < 1: break
            search_count_input = int(items_to_search)
            if search_count_input == 0: print('Enter a non zero number')
            elif search_count_input > search_count_all: print('Enter a number lower than the total API calls needed')
            elif (gas - search_count_input) < 800: print('Not enough API balance, try again')
            else:
                input_by_user_flag = 'yes'
                break
        except:
            print('Invalid data, please enter again or just press enter to quit: ')
    if len(items_to_search) < 1: quit()

if input_by_user_flag == 'yes': search_limit = search_count_input
else: search_limit = search_count_all

# Call the imdb API to get imdbID
print('Looking for '+ str(search_limit) + ' missing IMDB ID(s). . . . ')
print('Remaining API gas: ',gas)

for i in missing_imdbdata:
    counter = counter + 1
    if counter > search_limit: break
    imdbid = i[0]
    # format the query string and make the API call for each imdb ID
    querystring['i'] = imdbid
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        imdb_dict = {}
        js = response.json()
        if js['Response'] == 'True':
            imdb_dict = js
            imdb_dict['imdb_data_found'] = 'yes'
            table_imdb_found.append(imdb_dict)
            found_by_api = found_by_api + 1
        elif js['Response'] == 'False':
            imdb_dict['imdbID'] = imdbid
            imdb_dict['imdb_data_found'] = 'no'
            table_imdb_not_found.append(imdb_dict)
            not_found_by_api = not_found_by_api + 1

    # load the data in SQLITE (every few titles) and print the count
    if (counter % write_after) == 0:
        execute_sql3(table_imdb_found)
        execute_sql4(table_imdb_not_found)
        del table_imdb_found
        del table_imdb_not_found
        table_imdb_found = []
        table_imdb_not_found = []

# Load remaining titles if any
if len(table_imdb_found)>0:
    execute_sql3(table_imdb_found)
    del table_imdb_found
    table_imdb_found = []

if len(table_imdb_not_found)>0:
    execute_sql4(table_imdb_not_found)
    del table_imdb_not_found
    table_imdb_not_found = []

if search_limit > 0:
    print('IMDB IDs searched by API:', search_limit)
    print('IMDB IDs found by API:', found_by_api)
    print('IMDB IDs not found by API:', not_found_by_api)
