import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
import schedule
import time

def collect_and_update_data():
    # Step 1: Calculate the last 14 dates (mm/dd/yyyy)
    today = datetime.today()
    last_14_dates = [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(14)]
    last_14_dates.reverse()  # To order from oldest to most recent

    # Dates in the format of yyyy-mm-dd
    dates_for_url = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
    dates_for_url.reverse()  # To order from oldest to most recent

    # Base URL and API key used to access TMEIC Bugzilla materials handling database
    base_url = "https://tools.tmeic.com/mh/rest/bug"
    api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV" # Make sure to replace API key with your own for it to work

    # Create empty arrays to store data on normal-highest severity bugs over time
    Severe_Array = []
    High_Normal_Array = []

    # for loop iterates through all the last 14 dates to get both the critical/blocker bugs
    # and major/normal bugs from tmeic's mh bugzilla database
    for date in dates_for_url:
        # Links for severe and normal bugs
        urlSevere = f"{base_url}?severity=critical&severity=blocker&creation_time={date}&api_key={api_key}"
        urlHigh_Normal = f"{base_url}?severity=major&severity=normal&creation_time={date}&api_key={api_key}"

        #gets .json of severe bugs from bugzilla
        responseSevere = requests.get(urlSevere)
        dataSevere = responseSevere.json()
        print (dataSevere)

        #gets .json of high/normal severity bugs from bugzilla
        responseHigh_Normal = requests.get(urlHigh_Normal)
        dataHigh_Normal = responseHigh_Normal.json()

        # Initialize a counter for Severe open bugs
        open_Severe_bug_count = 0

        # Iterate through the list of bugs and count open bugs
        for bug in dataSevere["bugs"]:
            if bug["is_open"]:
                open_Severe_bug_count += 1

        # Initialize a counter for High/Normal open bugs
        open_High_Normal_bug_count = 0

        # Iterate through the list of bugs and count open bugs
        for bug in dataHigh_Normal["bugs"]:
            if bug["is_open"]:
                open_High_Normal_bug_count += 1

        # Appends the number of bugs on that date to the arrays
        Severe_Array.append(open_Severe_bug_count)
        High_Normal_Array.append(open_High_Normal_bug_count)

    # for loop to solve number of bugs created on a specific day
    # (bugs created since day minus bugs created since the next day)

    countSev = 0
    countHiNorm = 0
    for numSev in Severe_Array[:-1]:
        Severe_Array[countSev] = Severe_Array[countSev] - Severe_Array[countSev+1]
        High_Normal_Array[countHiNorm] = High_Normal_Array[countHiNorm] - High_Normal_Array[countHiNorm + 1]
        countSev += 1
        countHiNorm += 1

    """
    # Print the total count of open bugs to check accuracy
    print("Total Severe open bugs:", Severe_Array)
    print("Total Major/Normal open bugs", High_Normal_Array)

    # Print the different date formats to check accuracy
    print("Dates for URL links: ", dates_for_url)
    print("Bugs saved to Dates: ", last_14_dates)
    """

    # Formats dates and the two sets of bug severity counters into 3 columns
    data = {
        "Day": last_14_dates,
        "Blocker/Critical Bugs": Severe_Array,
        "Major/Normal Bugs": High_Normal_Array
    }

    # Create a DataFrame with the output
    df = pd.DataFrame(data)

    # Open the existing Excel file with macros (xlsm)
    output_file = "D:/OneDrive - TMEIC/Desktop/Bugzilla Tracker/TestEmaildoc.xlsm"
    app = xw.App(visible=False)
    wb = app.books.open(output_file)

    # Select the range of the table in the Excel sheet
    sheet_name = "Test1"  # Replace with the name of the sheet containing the table
    table_range = f"{sheet_name}!A2:C15"  # Replace with the range of your table (excluding headers)

    # Write the DataFrame to the selected table range without index and headers
    wb.sheets[sheet_name].range(table_range).value = df.values

    # Save and close the workbook
    wb.save()
    wb.close()

    # Quit the Excel application
    app.quit()

    """
    # Checks that output filepath is correct
    print("Output saved to", output_file)
    """

# Schedule the function to run at regular intervals (1440 minutes in a day, 30s-1min runtime, chose
# 1439 minutes for daily update)
schedule.every(1439).minutes.do(collect_and_update_data)

# Run the scheduled tasks indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)