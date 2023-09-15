# Author      : Aniruddh Chauhan
# Date Created: 09/14/2023
# Description : A python script that takes user input and searches for the closest issues. related to the keywords put in from Bugzilla

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
import tkinter as tk
from tkinter import ttk
import time  
import filter_keywords
from nltk.corpus import stopwords

pattern = r'\b[a-zA-Z]+\b'

base_url = "https://tools.tmeic.com/mh/rest/bug"
api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"
url = f"{base_url}?id&api_key={api_key}"
response = requests.get(url)
json_data = response.json()  # gets .json of bugs from bugzilla

common_words = set(stopwords.words('english'))
custom_stopwords = ["needs", "needs:", "Need" ,"instead", "be", "nothing", "something", 
                    "everything","check","need","due" , "ok", "OK", "Ok", "full", "new", 
                    "almost", "start", "lost", "moving", "reset", "restarts", "restart", 
                    "changes", "If", "if", "message", "end", ]
common_words.update(custom_stopwords)
common_words_list = list(common_words)

def search_components():    
    selected_option = option_var.get() # User selected search component 
    issue_count = 0
    issue_list = []

    for bug in json_data["bugs"]:
        if(bug ["component"] == selected_option):
            issue_list.append(bug["summary"])
            issue_count = issue_count + 1
       
    if (issue_count > 0):
        result_label.config(text="Success!\n")
    else:
        result_label.config(text="Sorry, Try Again :(\n")

    # Get Filtetred Data i.e. relevant Keywords 
    filtered_data = [filter_keywords.remove_words(summary, common_words_list) for summary in issue_list]
    filter_keywords.keyword_max_counter(filtered_data)
    
    keywords_set = set()
    for filtered_sum in filtered_data:
        valid_keyword = re.findall(pattern, filtered_sum)
        keywords_set.update(valid_keyword)
    keywords_list = list(keywords_set)

    with open("keyword_list.txt", "w") as keyword_file:
            for item in keywords_list:
                keyword_file.write(item + "\n")

     # Initialize empty lists for each keyword in the dictionary
    grouped_data = {}  
    for keyword in keywords_list:
        grouped_data[keyword] = []
        for bug in json_data["bugs"]:
            if keyword in bug["summary"].split():
                 grouped_data[keyword].append(bug["summary"])
 
                #  with open("grouped_issues_based_on_keywords.txt", "a", encoding="utf-8") as file:
                #         file.write(bug["summary"] + "\n")
    for keyword, summary_list in grouped_data.items():
        print(f"Keyword: {keyword}")
        print("Associated List:")
        for summary in summary_list:
            print(summary)
            print("\n")

    with open("component_fetch.txt", "w") as file1:
        for item in issue_list:
            file1.write(item + "\n")

    with open("component_fetch_filtered.txt", "w") as file2:
        for item in filtered_data:
            file2.write(item + "\n")

# Make the Window for the User Input 
GUI_window = tk.Tk()
GUI_window.title("JSON Component Search GUI")

option_label = ttk.Label(GUI_window, text="Select search option:")
option_label.pack()

search_options = ["Crane PLC", "Crane PLC","General", "Maxview"]
option_var = tk.StringVar()
option_var.set("Crane PLC")  # Set the default option
option_dropdown = ttk.OptionMenu(GUI_window, option_var, *search_options)
option_dropdown.pack()

# Create a button to perform the search
search_button = ttk.Button(GUI_window, text="Search", command = search_components)
search_button.pack()

result_label = ttk.Label(GUI_window, text="")
result_label.pack()
progress_bar = ttk.Progressbar(GUI_window, orient='horizontal',mode='determinate',length=280)
progress_bar.pack()
GUI_window.mainloop()











    