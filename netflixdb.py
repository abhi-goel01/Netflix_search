"""
Author: Abhishek Goel
Purpose: Read Netflix data and load into SQLITE database
"""

import requests
import json
from netflixfunc import *
import html

# Program variables
total = 0
count = 0
skipped = 0
write_after = 50
title_dict = {}
table_titles = []

while True:
    num_days = input('Enter the number of days for which you want to refresh the Netflix data: ')
    try:
        if len(num_days)<1: break
        days = int(num_days)
        if days > 1000: print('Greater than 1000 days not allowed, try again')
        else: break
    except:
        print('Invalid data, please enter again or just press enter to quit: ')
if len(num_days)<1: quit()

# Netflix API to retrieve content
# Load all titles released in India in last n days
url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
querystring = {"q":"get:new7:IN","p":"1","t":"ns","st":"adv"}
querystring["q"] = 'get:new'+str(days)+':'+'IN'
headers = {
    'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com",
    'x-rapidapi-key': "your key"
    }
response = requests.request("GET", url, headers=headers, params=querystring)

# If the API response is good, find out the total titles returned
# Also find out how many API rquests are remaining from the limit
if response.status_code == 200:
    js = response.json()
    total = int(js['COUNT'])
    # calculate the number of pages in which our result will be spanned, each page returns max 100 items
    pages = (total//100)+1
    remainder = (total%100)
    limit = int(response.headers['x-ratelimit-requests-limit'])
    gas = int(response.headers['x-ratelimit-requests-remaining'])
    # See if we have sufficient calls remaining from our quota to process this request, keeping a buffer of 20 calls
    if (gas-pages) < 2:
        print("\033[91m{}\033[00m".format('Not enough API balance, Either decrease the number of days or try again tomorrow, quitting . . .'))
        print('API daily limit:',limit)
        print('API calls remaining for today:',gas)
        print('API calls needed:',pages)
        print('Buffer kept:','20')
        quit()

    # Here are the color codes for printing output
    # "\033[91m{}\033[00m" - Red
    # "\033[92m{}\033[00m" - Green
    # "\033[93m{}\033[00m" - Yellow
    # "\033[94m{}\033[00m" - Light Purple
    # "\033[95m{}\033[00m" - Purple
    # "\033[96m{}\033[00m" - Cyan
    # "\033[97m{}\033[00m" - Light gray

# For all the pages that contain the data
for page in range(1,pages+1):
    # For all the titles returned per page
    if page < pages: upper = 100
    else: upper = remainder
    for title in range(0,upper):
        # Check and see if the title already exists in our DB and only load new ones
        flag = check_if_exists(js['ITEMS'][title]['netflixid'])
        if flag == 'Exists':
            skipped = skipped + 1
            continue

        # Append the title information available as a dictionary object into an internal list of dictionaries
        title_dict = js['ITEMS'][title]
        # Convert HTML characters to normal characters before writing into dB and clean up synopsis
        title_dict['title'] = html.unescape(title_dict['title'])
        title_dict['synopsis'] = html.unescape(title_dict['synopsis']).split('<br>')[0]
        # If there is no imdbID returned from Netflix API, move no to the searched column
        # We will later try to find out the imdbID using imdb API
        if title_dict['imdbid'] == '' or title_dict['imdbid'] == 'notfound':
            title_dict['searched'] = 'no'
            title_dict['imdbid'] = ''
        else:
            title_dict['searched'] = 'n/a'
        table_titles.append(title_dict)
        count = count + 1

        # load the data in SQLITE (every few titles) and print the count
        if (count % write_after) == 0:
            execute_sql(table_titles)
            del table_titles
            table_titles = []

    # Load remaining titles if any
    if len(table_titles)>0:
        execute_sql(table_titles)
        del table_titles
        table_titles = []

    if page != pages:
        querystring['p'] = page
        print(querystring)
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            js = response.json()

print('-----------------------------------------------')
print('No. of titles read from Netflix API:',total)
print('No. of titles skipped:',skipped)
print('No. of titles loaded in DB:',count)
print('-----------------------------------------------')
