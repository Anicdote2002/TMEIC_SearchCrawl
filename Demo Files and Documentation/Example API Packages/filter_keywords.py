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

def preprocess_text(text):
    # Remove punctuation and extra whitespace while preserving case
    text = re.sub(r'[^\w\s]', '', text)
    return text

def preprocess_filter_words(words_to_filter):
    # Remove punctuation and extra whitespace while preserving case for each word
    return [re.sub(r'[^\w\s]', '', word) for word in words_to_filter]

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

