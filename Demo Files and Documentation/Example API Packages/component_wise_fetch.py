import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
from PIL import Image
from collections import defaultdict, Counter
import os
import re

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

    


print("Number of Crane PLC Issues: ", cranePLC_issue_count)
print("Number of Maxview Issues  : ", maxview_issue_count )
print("Number of General Issues  : ", general_issue_count )
