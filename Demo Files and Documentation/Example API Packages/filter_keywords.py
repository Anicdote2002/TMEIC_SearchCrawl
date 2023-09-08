# Author      : Aniruddh Chauhan
# Data Created: 09/08/2023
# Description : A python to filter out words from the 'summary' field in the json file outputs from bugzilla
import json
import os
# open json file for reading. 
print("Current working directory:", os.getcwd())
json_file = open('.\Example API Packages\data1.json')


# returns JSON object as a dictionary 
# Credits- geeksforgeeks.org 
json_data = json.load(json_file)
common_words = [" The", "in", "on"] #expand this in the future


for i in json_data['bugs']:
    print(i)
 
# Closing file
json_file.close()

