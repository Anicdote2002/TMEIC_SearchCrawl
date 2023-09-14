
import re
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
from PIL import Image
from collections import defaultdict
import os

print(re.split(r'\W+', 'Words, words, words. ')) # non-word character
print(re.split(r'\s+', 'Words, words, words. ')) # space character
print(re.split(r'\W+', 'Words, words, words'))

# with open('.\Example API Packages\data3.json', 'r', encoding='utf-8') as json_file:
# json_data = json.load(json_file)
# json_file = open('.\Example API Packages\data3.json')
# returns JSON object as a dictionary 
# Credits- geeksforgeeks.org 
# json_data = json.load(json_file)
print("Current working directory:", os.getcwd())
temp = defaultdict(int)
# for sub in filtered_data:
#     for wrd in re.split(r'\W+', sub):
#         temp[wrd] += 1
 
# # getting and printing max frequency
# res = max(temp, key=temp.get)
# print("Word with maximum frequency: " + str(res))


text = "This is Some sample Text with MixeD case WoRds."

# Convert the text to lowercase
text = text.lower()

# List of words to remove (in lowercase)
words_to_remove = ["this", "sample", "with"]

# Split the text into words
words = text.split()

# Remove words from the list of words to remove
filtered_words = [word for word in words if word not in words_to_remove]

# Join the remaining words back into a string
filtered_text = " ".join(filtered_words)

print(filtered_text)



# Create a list to store the filtered words
filtered_word_2 = []

# Iterate through the words in the text
for word in words:
    # Check if the lowercase version of the word is in the list of words to remove
    if word.lower() not in words_to_remove:
        filtered_word_2.append(word)  # Keep the word with its original case
    else:
        filtered_word_2.append("")  # Replace removed words with an empty string

# Join the remaining words back into a string
filtered_text_2 = " ".join(filtered_word_2)

print(filtered_text_2)