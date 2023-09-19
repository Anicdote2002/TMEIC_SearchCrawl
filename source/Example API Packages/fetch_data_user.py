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
import fetch_data_functions
from nltk.corpus import stopwords

pattern = r'\b[a-zA-Z]+\b'
json_data = fetch_data_functions.get_json_data()
common_words_list = fetch_data_functions.generate_common_stopwords()

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

    # Pre process all text to get rid of any punctuation, whitespace"
    pre_common_words_list = fetch_data_functions.preprocess_filter_words(common_words_list)
    pre_issue_list = [fetch_data_functions.preprocess_text(sentence) for sentence in issue_list]
    # Get Filtetred Data i.e. relevant Keywords 
    filtered_data  = [fetch_data_functions.remove_words(summary, pre_common_words_list) for summary in pre_issue_list]
    fetch_data_functions.keyword_max_counter(filtered_data)
    
    # Generate Keyword List and Output list in a txt file
    unique_keywords_set = set() 
    repeated_keywords_list = []

    for filtered_sum in filtered_data:
        valid_keyword = re.findall(pattern, filtered_sum) 
        unique_keywords_set.update(valid_keyword)   
        repeated_keywords_list.extend(valid_keyword)  

    unique_keywords_list = list(unique_keywords_set) 
    top_keywords_list = fetch_data_functions.get_top_keywords(repeated_keywords_list, 20) # Sus, Redo this line

    with open("keyword_list.txt", "w") as keyword_file:
            for item in unique_keywords_list:
                keyword_file.write(item + "\n") 
    with open("top_keywords.txt", "w") as top_keywords_file:
        for keyword, count in top_keywords_list:
            top_keywords_file.write(f"{keyword}: {count}\n")

    # Initialize empty dictionary for grouping summaries based on each keyword in the dictionary
    grouped_summaries = {}  
    grouped_bug_ids   = {}
    # grouped_comments  = {}
    for keyword in unique_keywords_list:
        grouped_summaries[keyword] = [] # Initialize an Empty list for similar summaries with the keywords as the key in the dictionary i.e. <key>Keyword <value>Summaries List
        grouped_bug_ids  [keyword] = [] # Initialize an Empty list for similar summaries's bug ids with the keywords as the key in the dictionaryi.e. <key>Keyword <value>Bug IDs List
      # grouped_comments [keyword] = []
        for bug in json_data["bugs"]:
            if (bug ["component"] == selected_option): 
                if keyword in bug["summary"].split():
                   grouped_summaries[keyword].append(bug["summary"]) # Append to list of the summaries under a particular keyword
                   grouped_bug_ids  [keyword].append(bug["id"])      # Append to list of the bug ids
                  # grouped_comments [keyword].append(bug["comment"]) 

    with open("grouped_issues_based_on_keywords.txt", "w", encoding="utf-8") as file:
        pass
    with open("grouped_issues_based_on_keywords.txt", "a", encoding="utf-8") as file:
        for (keyword_summary, summary_list), (keyword_bug_id, bug_id_list) in zip(grouped_summaries.items(), grouped_bug_ids.items()):
            # A complicated way of accessing a number of lists associated to a particular key.
            file.write(f"Keyword_Summary: {keyword_summary}"+ "\n")
            file.write(f"Keyword_Bug_ID : {keyword_bug_id }"+ "\n")
            file.write("Associated Summaries:"+ "\n")
            for bug_id, summary in zip(bug_id_list, summary_list):
                file.write(f"Summary:- {summary} | Bug ID:- {bug_id}" + "\n")
            file.write("\n")
        
    with open("component_fetch.txt", "w") as file1:
        for item in issue_list:
            file1.write(item + "\n")

    with open("component_fetch_filtered.txt", "w") as file2:
        for item in filtered_data:
            file2.write(item + "\n")
      
def display_keywords():
    root = tk.Tk()
    root.title("Keywords List")
    # Create a Text widget to display the file contents
    text_widget = tk.Text(root, wrap="none")  # wrap="none" to disable text wrapping
    text_widget.pack(fill="both", expand=True)  # fill the entire window
    # Open and read the text file
    file_path = r"C:\Users\Aniruddh.Chauhan\Documents\Bugzilla Data Mining\source\keyword_list.txt"  # Replace with the path to your text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
            text_widget.insert("1.0", file_contents)  # Insert the file contents into the Text widget
    except FileNotFoundError:
        text_widget.insert("1.0", "File not found.")
    # Start the Tkinter main loop
    root.mainloop()
def display_top_keywords():
    root = tk.Tk()
    root.title("Keywords List")
    # Create a Text widget to display the file contents
    text_widget = tk.Text(root, wrap="none")  # wrap="none" to disable text wrapping
    text_widget.pack(fill="both", expand=True)  # fill the entire window
    # Open and read the text file
    file_path = r"C:\Users\Aniruddh.Chauhan\Documents\Bugzilla Data Mining\source\top_keywords.txt"  # Replace with the path to your text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
            text_widget.insert("1.0", file_contents)  # Insert the file contents into the Text widget
    except FileNotFoundError:
        text_widget.insert("1.0", "File not found.")
    # Start the Tkinter main loop
    root.mainloop()
def display_grouped_data():
    root = tk.Tk()
    root.title("Text File Viewer")
    # Create a Text widget to display the file contents
    text_widget = tk.Text(root, wrap="none")  # wrap="none" to disable text wrapping
    text_widget.pack(fill="both", expand=True)  # fill the entire window
    # Open and read the text file
    file_path = r"C:\Users\Aniruddh.Chauhan\Documents\Bugzilla Data Mining\source\grouped_issues_based_on_keywords.txt"  # Replace with the path to your text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
            text_widget.insert("1.0", file_contents)  # Insert the file contents into the Text widget
    except FileNotFoundError:
        text_widget.insert("1.0", "File not found.")
    # Start the Tkinter main loop
    root.mainloop()

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
display_button = ttk.Button(GUI_window, text="Output", command = display_grouped_data)
display_button.pack()
keywords_button = ttk.Button(GUI_window, text="Keywords", command = display_keywords)
keywords_button.pack()
top_keywords_button = ttk.Button(GUI_window, text="Top Keywords", command = display_top_keywords)
top_keywords_button.pack()
result_label = ttk.Label(GUI_window, text="")
result_label.pack()
progress_bar = ttk.Progressbar(GUI_window, orient='horizontal',mode='determinate',length=280)
progress_bar.pack()
GUI_window.mainloop()











    