# Author      : Aniruddh Chauhan
# Date Created: 09/08/2023
# Description : A python script to filter out words from the 'summary' field in the json file outputs from Bugzilla
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
from PIL import Image
from collections import defaultdict, Counter
import os
import re
import nltk
from nltk.corpus import stopwords

def remove_words(summary, words):
    for word in words:      
        summary = summary.replace(f' {word} ', ' ')  
    return summary.strip()
# Remove the common words from each sentence in the list and store the modified sentences
def keyword_max_counter(filtered_data):
    all_filtered_data = " ".join(filtered_data)
    cleaned_filtered_data = re.sub(r'[^\w\s]', '', all_filtered_data)
    filtered_data_wrds = cleaned_filtered_data.split()# Tokenize the large string into words (split by space)
    word_counts = Counter(filtered_data_wrds)# Count the frequency of each word
    max_word, max_count = word_counts.most_common(1)[0]# Find the word with the maximum frequency
# The reason we are strupping common words is because we the keywords are A LOT. 
# Therefore, a solution to that is to strip all the common words
# common_words = ["The"   , "in"   , "on"    , "were"  , "of"    , "not"    ,
#                 "to"    , "is"   , "a"     , "as"    , "an"    , "that"   , 
#                 "the"   , "and"  , "but"   , "has"   , "have"  , "move"   ,
#                 "where" , "was"  , "can"   , "cannot", "be"    , "In"     ,
#                 "should", "would", "could" , "with"  , "for"   , "if"     ,
#                 "when"  , "what" , "after" , "into"  , "update", "between",
#                 "why"   , "color", "scheme", "test"  , "do "   , "from"  
#                 "been"  , "issue", "needs" , "need"                        ] #expand this in the future

common_words = set(stopwords.words('english'))
custom_stopwords = ["needs"]
common_words.update(custom_stopwords)
common_words_list = list(common_words)

base_url = "https://tools.tmeic.com/mh/rest/bug"
api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"
url = f"{base_url}?id&api_key={api_key}"

response = requests.get(url)
json_data = response.json() # gets .json of bugs from bugzilla

bug_sum_list = []
for bug_sum in json_data["bugs"]:
    bug_sum_list.append(bug_sum["summary"])


filtered_data = [remove_words(summary, common_words_list) for summary in bug_sum_list]
keyword_max_counter(filtered_data)