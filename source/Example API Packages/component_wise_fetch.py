# Author      : Aniruddh Chauhan
# Date Created: 09/08/2023
# Description : A python script to generate issues from the different componets file outputs from Bugzilla

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
import filter_keywords
from nltk.corpus import stopwords


common_words = set(stopwords.words('english'))
custom_stopwords = ["needs", "needs:", "Need" ,"instead", "be", "nothing", "something", 
                    "everything","check","need","due" , "ok", "OK", "Ok", "full", "new", 
                    "almost", "start", "lost", "moving", "reset", "restarts", "restart", 
                    "changes", "If", "if", "message", "end", "moves", "going", "move", 
                    "laptop", "invalid", "site", "required", "require", "working", "releases"
                    "Using", "setup", "TMEIC", "computer", "match", "Add", "add", "model", "crashes",
                    "parameter", "Parameter", "target", "DISK", "disk", "scan", "data","calculation",
                    "restart", "model", "stuck", "state", "Anti", "Control", "control", "lost"]
common_words.update(custom_stopwords)
common_words.update(custom_stopwords)
common_words_list = list(common_words)

base_url = "https://tools.tmeic.com/mh/rest/bug"
api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"
url = f"{base_url}?id&api_key={api_key}"
response = requests.get(url)
json_data = response.json() # gets .json of bugs from bugzilla

cranePLC_issue_count = 0
maxview_issue_count  = 0
general_issue_count  = 0

bug_cranePLC_list = []
bug_maxview_list  = []
bug_general_list  = []

for bug_comp in json_data["bugs"]:
    if(bug_comp["component"] == "Crane PLC"):
        bug_cranePLC_list.append(bug_comp["summary"])
        cranePLC_issue_count = cranePLC_issue_count + 1

    elif(bug_comp["component"] == "Maxview"):
        bug_maxview_list.append(bug_comp["summary"])
        maxview_issue_count = maxview_issue_count + 1

    elif(bug_comp["component"] == "General"):
        bug_general_list.append(bug_comp["summary"])
        general_issue_count = general_issue_count + 1


with open("output_bug_cranePLC_list.txt", "w") as file1:
    for item in bug_cranePLC_list:
        file1.write(item + "\n")

# Output list2 to a text file
with open("output_bug_maxview_list.txt", "w") as file2:
    for item in bug_maxview_list:
        file2.write(item + "\n")

# Output list3 to a text file
with open("output_bug_general_list.txt", "w") as file3:
    for item in bug_general_list:
        file3.write(item + "\n")


# Get Filtetred Data i.e. relevant Keywords
cranePLC_filtered_data = [filter_keywords.remove_words(summary_cranePLC, common_words_list) for summary_cranePLC in bug_cranePLC_list]
maxview_filtered_data  = [filter_keywords.remove_words(summary_Maxview, common_words_list)  for summary_Maxview  in bug_maxview_list ]
general_filtered_data  = [filter_keywords.remove_words(summary_General, common_words_list)  for summary_General  in bug_general_list ]

filter_keywords.keyword_max_counter(cranePLC_filtered_data)
filter_keywords.keyword_max_counter(maxview_filtered_data)
filter_keywords.keyword_max_counter(general_filtered_data)

with open("output_keyword_cranePLC_list.txt", "w") as keyword_file1:
    for item in cranePLC_filtered_data:
        keyword_file1.write(item + "\n")

# Output list2 to a text file
with open("output_keyword_maxview_list.txt", "w") as keyword_file2:
    for item in maxview_filtered_data:
        keyword_file2.write(item + "\n")

# Output list3 to a text file
with open("output_keyword_general_list.txt", "w") as keyword_file3:
    for item in general_filtered_data:
        keyword_file3.write(item + "\n")
                            
print("Number of Crane PLC Issues: ", cranePLC_issue_count)
print("Number of Maxview Issues  : ", maxview_issue_count )
print("Number of General Issues  : ", general_issue_count )
