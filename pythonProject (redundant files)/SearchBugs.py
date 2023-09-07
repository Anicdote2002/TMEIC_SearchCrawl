import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw

print("Enter the following data fields to determine the number of closed bugs (optional)")
product = input("Enter the project:\n")
component = input("Enter the component:\n")
severity = input("Enter the severity of the bug:\n")
date = input("Enter the date created (yyyy-mm-dd; all bugs since that date will be returned):\n")

# Base URL and api key used to access TMEIC Bugzilla materials handling database
base_url = "https://tools.tmeic.com/mh/rest/bug"
api_key = "JrfGl8dx6tbK331csReq63YrP02yQ0PFUKceJUtS"

url_noDate = f"{base_url}?product={product}&component={component}&severity={severity}&api_key={api_key}"       # &creation_time={date}&api_key={api_key}"
url_Date = f"{base_url}?product={product}&component={component}&severity={severity}&creation_time={date}&api_key={api_key}"

if not (date and date.strip()):
    url = url_noDate

else:
    url = url_Date

# gets .json of severe bugs from bugzilla
response = requests.get(url)
data = response.json()

# Initialize a counter for closed bugs
count = 0
# Iterate through the list of bugs and count closed bugs
for bug in data["bugs"]:
    if not bug["is_open"]:
        count += 1

print("\n\nThe number of closed bugs for\n\nproduct: ", product, "\nseverity: ", severity, "\n\nis: ", count)