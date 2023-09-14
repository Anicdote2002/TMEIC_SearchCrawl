# Author      : Aniruddh Chauhan
# Date Created: 09/08/2023
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




def search_components():
    
    selected_option = option_var.get() # User selected search component

    base_url = "https://tools.tmeic.com/mh/rest/bug"
    api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"
    url = f"{base_url}?id&api_key={api_key}"
    response = requests.get(url)
    json_data = response.json() # gets .json of bugs from bugzilla
    
    common_words = set(stopwords.words('english'))
    custom_stopwords = ["needs", "needs:", "Need" ,"instead", "be", "nothing", "something", "everything","check","need","due"]
    common_words.update(custom_stopwords)
    common_words_list = list(common_words)

    start_time = time.time()

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
    
    end_time = time.time()
    runtime = round(end_time - start_time, 2)
    progress_bar['value'] = runtime


# Make the Window for the User Input 
GUI_window = tk.Tk()
GUI_window.title("JSON Component Search GUI")

option_label = ttk.Label(GUI_window, text="Select search option:")
option_label.pack()

search_options = ["Crane PLC", "General", "Maxview"]
option_var = tk.StringVar()
option_var.set(search_options[0])  # Set the default option
option_dropdown = ttk.OptionMenu(GUI_window, option_var, *search_options)
option_dropdown.pack()

# Create a button to perform the search
search_button = ttk.Button(GUI_window, text="Search", command = search_components)
search_button.pack()

result_label = ttk.Label(GUI_window, text="")
result_label.pack()
progress_bar = ttk.Progressbar(GUI_window, length=300, mode='determinate')
progress_bar.pack()
GUI_window.mainloop()











    