
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