#!/usr/bin/env python
# coding: utf-8

import re
import numpy as np
import pandas as pd
import datetime as dt
import sys
import requests
from math import ceil

counter = 0

# Obtain an API key and use the below API call to The Guardian
# and edit the variable below

API_KEY = 'YOUR-API-KEY-HERE'

# The Guardian API has a set 'page size' limit of 50

search_query1 = 'analytics'
search_query2 = 'AI'
page_size = 5
starting_page = 1

# initial query to check for the volume of responses
# variables from above are input into the search query
search_query = f'{search_query1}%20AND%20{search_query2}'

url = 'https://content.guardianapis.com/search?q={}&api-key={}&page-size={}&page={}'.format(
    search_query,
    API_KEY,
    page_size,
    starting_page
)

results = requests.get(url).json()

def get_all_the_articles(page_number):
    """Create a Pandas dataset for a given API page number."""
    
    url = 'https://content.guardianapis.com/search?q={}&api-key={}&page-size={}&page={}&order-by=newest'.format(
        search_query,
        API_KEY,
        page_size,
        page_number
    )
    print(url)
   
    results = requests.get(url).json()
    
    global counter
    counter += 1
    
    temp_results = results['response']['results']
    
    temp_df = pd.DataFrame(temp_results)
    
    return temp_df


# We loop through the page number list and apply our function to each page in the list. 
# The loop creates a temporary dataframe, for each request and results are appended to the main dataframe (df).

df = pd.DataFrame()

# In order to iterate on all pages, we need to know how many pages are returned
# in our query. We make an initial request to page 1 in order to get the total
# number of pages from `results['response]['pages]`.

initial_data = get_all_the_articles(1)
total_pages = results['response']['pages']

# We use the total number of pages to build a range to iterate on.

for page_number in range(1, total_pages+1):
    
    temp_df = get_all_the_articles(page_number)
    
    temp_df['counter'] = counter
    
    df = df.append(temp_df, ignore_index=True)
    

# This non-cleaned dataframe (df) is sent to guardian_original.csv for backup.

df.to_csv('guardian_original.csv', index=False)


# Read the 'guardian_original.csv' as df1

df1 = pd.read_csv('guardian_original.csv', keep_default_na=False)


# Sort the dataframe df1 by webPublicationDate in descending order

# Please note that I tried adding the "order-by" query parameter to the API,
# but the results still seem to be unordered, so I am also sorting the data
# in the dataframe in order to be sure that data is correctly sorted.

df1['webPublicationDate'] = df1['webPublicationDate'].astype('datetime64[ns]')
df1.sort_values(by=['webPublicationDate'], inplace=True, ascending=False)

# (1) Create a new 'formatted_date' column of 'webPublicationDate' in day/month/year
# format in `df1`.
df1['formatted_date'] = df1["webPublicationDate"].dt.strftime("%d/%m/%Y")

# (2) Create a new column 'year' with the year from 'webPublicationDate' or 'formatted_date'.
df1['year'] = df1["webPublicationDate"].dt.strftime("%Y")

# (3) Re-format the column headers of df2 to snake_case.
def camelcase_to_snake(column_name):
    """Transform col headers from camelCase to snake_case."""
    cap_first_word = f'{column_name[0].upper()}{column_name[1:]}'
    single_words = re.findall('[A-Z][^A-Z]*', cap_first_word)
    return "_".join(single_words).lower()

df1.columns = df1.columns.to_series().apply(camelcase_to_snake)

# Output final dataframe (df2) to guardian_final.csv
df1.to_csv('guardian_final.csv', index=False)
