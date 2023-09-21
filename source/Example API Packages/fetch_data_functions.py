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
import tkinter as tk
from tkinter import ttk

def get_json_data():
    base_url = "https://tools.tmeic.com/mh/rest/bug"
    api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"
    url = f"{base_url}?id&api_key={api_key}"
    response = requests.get(url)
    json_data = response.json()  # gets .json of bugs from bugzilla
    return json_data

def generate_common_stopwords():
    common_words = set(stopwords.words('english'))
    custom_stopwords = ["needs"     , "needs:"      , "Need"    ,"instead"      , "be"      , "nothing" , "something"   , "State"       ,"reporting" ,
                        "everything", "check"       , "need"    ,"due"          , "ok"      , "OK", "Ok", "full"        , "new"         ,"stops"     ,
                        "almost"    , "start"       , "lost"    , "moving"      , "reset"   , "restarts", "restart"     , "full"        ,"offset"    ,
                        "changes"   , "If"          , "if"      , "message"     , "end"     , "moves"   , "going"       , "move"        ,"initial"   ,
                        "laptop"    , "invalid"     , "site"    , "required"    , "require" , "working" , "releases"    , "crashes"     ,"position"  ,
                        "Using"     , "setup"       , "TMEIC"   , "computer"    , "match"   , "Add"     , "add"         , "model"       ,"host"      , 
                        "parameter" , "Parameter"   , "target"  , "DISK"        , "disk"    , "scan"    , "data"        ,"calculation"  ,"testing"   ,
                        "restart"   , "model"       , "stuck"   , "state"       , "Anti"    , "Control" , "control"     , "lost"        , 
                        "angle"     , "include"     , "full"    , "direction"   , "file"    , "spare"   , "done"        , "address"     , "Using"]
                        
    common_words.update(custom_stopwords)
    common_words_list = list(common_words)
    return common_words_list

def preprocess_text(text):
    # Remove punctuation and extra whitespace while preserving case
    text = re.sub(r'[^\w\s]', '', text)
    return text

def preprocess_filter_words(words_to_filter):
    # Remove punctuation and extra whitespace while preserving case for each word
    return [re.sub(r'[^\w\s]', '', word) for word in words_to_filter]

def remove_words(summary, words):
    for word in words:      
        summary = re.sub(r'\b%s\b' % f'{word}', '', summary)
    return summary.strip()
# Remove the common words from each sentence in the list and store the modified sentences
def keyword_max_counter(filtered_data):
    all_filtered_data = " ".join(filtered_data)
    cleaned_filtered_data = re.sub(r'[^\w\s]', '', all_filtered_data)
    filtered_data_wrds = cleaned_filtered_data.split()# Tokenize the large string into words (split by space)
    word_counts = Counter(filtered_data_wrds)# Count the frequency of each word
    max_word, max_count = word_counts.most_common(1)[0]# Find the word with the maximum frequency

def get_top_keywords(keyword_list, top_n=20): 
    keyword_counts = Counter(keyword_list) # Count the occurrences of each keyword
    top_keywords = keyword_counts.most_common(top_n)  # Get the top N keywords
    return top_keywords
