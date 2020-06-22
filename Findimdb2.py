"""
Author: Abhishek Goel
Purpose: using API 2, Find imdb ID for the Netflix titles missing the same
"""

import requests
import json
from netflixfunc import *

#Program variables
missing_imdb = []
missing_imdb_result = []
total_items = 0
found_by_api2 = 0
search_count_input = 0
search_count_all = 0
input_by_user_flag = 'no'
counter = 0


# Search the database for titles with no imdbID
# Missing_imdb is a list of tuples containing title and its netflix id
missing_imdb = find_missing_imdbid('api2')
search_count_all = len(missing_imdb)

# If there are no netflix IDs with missing imdb ID then quit
if search_count_all < 1:
    print('No netflix IDs with missing IMDB ID, quitting . . .')
    quit()

# imdb API to retrieve content
url = "https://imdb8.p.rapidapi.com/title/find"
querystring = {"q":"title name"}
headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "your key"
    }

# Make one dummy call to find out the API calls remaining
querystring['q'] = 'the'
response = requests.request("GET", url, headers=headers, params=querystring)
api_limit = int(response.headers['x-ratelimit-requests-limit'])
gas = int(response.headers['x-ratelimit-requests-remaining'])

# See if we have sufficient calls remaining from our quota to process this request, keeping a buffer of 20 calls
if (gas-search_count_all) < 20:
    print("\033[91m{}\033[00m".format('Not enough API balance remaining to look for all missing imdb IDs . . .'))
    print('API monthly limit:',api_limit)
    print('API calls remaining for this month:',gas)
    print('API calls needed:',search_count_all)
    print('Buffer kept:','20')
    while True:
        items_to_search = input('Enter the number of titles you want to search or hit enter to quit: ')
        try:
            if len(items_to_search) < 1: break
            search_count_input = int(items_to_search)
            if search_count_input == 0: print('Enter a non zero number')
            elif search_count_input > search_count_all: print('Enter a number lower than the total API calls needed')
            elif (gas - search_count_input) < 20: print('Not enough API balance, try again')
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

for i in missing_imdb:
    counter = counter + 1
    if counter > search_limit: break
    title = i[0]
    flix_id = i[1]
    # format the query string and make the API call for each title
    querystring['q'] = title
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        tupl = ()
        js = response.json()
        try: total_items = len(js['results'])
        except: total_items = 0
        if total_items > 0:
            # If number of matches found by the API is more than 10 then limit the comparison to only 10 items
            # hopefully our title should be within the first 10 matches
            if total_items > 10: total_items = 10
            for item in range(0,total_items):
                try:
                    # Before comparing the titles convert them into lower case and suppress any whitespaces in between
                    if js['results'][item]['title'].lower().replace(" ", "") != title.lower().replace(" ", ""): continue
                    tupl = (flix_id, js['results'][item]['id'].split('/')[2], 'api2-found')
                    found_by_api2 = found_by_api2 + 1
                    missing_imdb_result.append(tupl)
                    break
                except:
                    continue
        if len(tupl) < 1:
            tupl = (flix_id, '', 'api2-not found')
            missing_imdb_result.append(tupl)

# Update the netflix tables with the imdbID found by the API
if len(missing_imdb_result) > 0: execute_sql2(missing_imdb_result)
if search_limit > 0:
    print('IMDB IDs searched by API 2:', len(missing_imdb_result))
    print('IMDB IDs found by API 2:', found_by_api2)
if counter > search_limit: quit()
