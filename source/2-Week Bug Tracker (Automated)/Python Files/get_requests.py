import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
import schedule
import time


   
base_url = "https://tools.tmeic.com/mh/rest/bug"    
api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV" # Make sure to replace API key with your own for it to work

    # Create empty arrays to store data on normal-highest severity bugs over time
    
urlSevere      = f"{base_url}?severity=critical&api_key={api_key}"    

#gets .json of severe bugs from bugzilla

responseSevere = requests.get(urlSevere)
data = responseSevere.json()
print (data)


      
   