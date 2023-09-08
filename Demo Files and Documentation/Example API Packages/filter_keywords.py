# Author      : Aniruddh Chauhan
# Data Created: 09/08/2023
# Description : A python to filter out words from the 'summary' field in the json file outputs from bugzilla
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
from PIL import Image
import os
# open json file for reading. 
# for future context, this will be changed to use the requests lib from python that pulls json data directly from the web 

base_url = "https://tools.tmeic.com/mh/rest/bug"
api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"

url = f"{base_url}?id&api_key={api_key}"

# gets .json of bugs from bugzilla
response = requests.get(url)
json_data = response.json()

print("Current working directory:", os.getcwd())

# with open('.\Example API Packages\data3.json', 'r', encoding='utf-8') as json_file:
# json_data = json.load(json_file)
# json_file = open('.\Example API Packages\data3.json')
# returns JSON object as a dictionary 
# Credits- geeksforgeeks.org 
# json_data = json.load(json_file)

# The reason we are strupping common words is because we the keywords are A LOT. 
# Therefore, a solution to that is to strip all the common words

common_words = ["The"   , "in"   , "on"   , "were"  ,"of"  ,"not" ,
                "to"    , "is"   , "a"    , "as"    ,"an"  ,"that", 
                "the"   , "and"  , "but"  , "has"   ,"have","move",
                "where" , "was"  , "can"  , "cannot","be"
                "should", "would", "could", "with"  ,"for"         ] #expand this in the future

bug_sum_list = []

for bug_sum in json_data["bugs"]:
    bug_sum_list.append(bug_sum["summary"])

filtered_data = []

def remove_words(summary, words):
    for word in words:
        replacement = ' ' * len(word)
        summary = summary.replace(f' {word} ', replacement)  
    return summary.strip()  # Strip and Replace the word with space

# Remove words from each sentence and store the modified sentences
filtered_data = [remove_words(summary, common_words) for summary in bug_sum_list]

# Print the modified sentences
for j in filtered_data:
    print(j)

