import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import xlwings as xw
from PIL import Image
import os

def run_script(product, component, severity):
    """
        Fetch bug data from Bugzilla API, analyze, and save results.

        Args:
            product (str): The project or product name.
            component (str): The component within the product.
            severity (str): The severity of the bug.

        Returns:
            Chart generated in Excel
        """

    # Step 1: Calculate the last 14 dates (mm/dd/yyyy)
    today = datetime.today()
    last_14_dates = [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(14)]
    last_14_dates.reverse()  # To order from oldest to most recent

    # Dates in the format of yyyy-mm-dd
    dates_for_url = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
    dates_for_url.reverse()  # To order from oldest to most recent

    # Base URL and api key used to access TMEIC Bugzilla materials handling database
    base_url = "https://tools.tmeic.com/mh/rest/bug"
    api_key = "9yvSoV8p575uVbPhPxgX9vIqJDbzatyuwMKlTrFV"

    # Create empty arrays to store data on bugs over time
    open_bug_Array = []
    closed_bug_Array = []

    # for loop iterates through all the last 14 dates to get both the open bugs
    # and closed bugs from TMEIC's mh bugzilla database
    for date in dates_for_url:
        # Links for severe and normal bugs
        url = f"{base_url}?product={product}&component={component}&severity={severity}&creation_time={date}&api_key={api_key}"

        # gets .json of bugs from bugzilla
        response = requests.get(url)
        data = response.json()
        //print (data)

        # Initialize a counter for open bugs
        open_bug_count = 0
        # Initialize a counter for closed bugs
        closed_bug_count = 0

        # Iterate through the list of bugs and count open/closed bugs
        for bug in data["bugs"]:
            if bug["is_open"]:
                open_bug_count += 1
            else:
                closed_bug_count += 1

        # Appends the number of bugs on that date to the arrays
        open_bug_Array.append(open_bug_count)
        closed_bug_Array.append(closed_bug_count)

    # for loop to solve number of bugs created on a specific day
    # (bugs created since day minus bugs created since the next day)
    open_count = 0
    closed_count = 0
    for num in open_bug_Array[:-1]:
        open_bug_Array[open_count] = open_bug_Array[open_count] - open_bug_Array[open_count+1]
        open_count += 1
        closed_bug_Array[closed_count] = closed_bug_Array[closed_count] - closed_bug_Array[closed_count + 1]
        closed_count += 1


    # Formats dates and the two sets of bug severity counters into 3 columns
    data = {
        "Day": last_14_dates,
        "Open Bugs": open_bug_Array,
        "Closed Bugs": closed_bug_Array
    }

    # Create a DataFrame with the output
    df = pd.DataFrame(data)

    # Open the existing Excel file (xlsx)
    output_file = "D:/OneDrive - TMEIC/Desktop/Bugzilla Tracker/SearchedBugsPlot.xlsx"  # this file path works only on TMEIC devices (OneDrive - TMEIC)
    app = xw.App(visible=False)
    wb = app.books.open(output_file)

    # Select the range of the table in the Excel sheet
    sheet_name = "Sheet1"  # Replace with the name of the sheet containing the table
    table_range = f"{sheet_name}!A2:C15"  # Replace with the range of your table (excluding headers)

    # Write the DataFrame to the selected table range without index and headers
    wb.sheets[sheet_name].range(table_range).value = df.values

    # Assuming your chart is located on Sheet1 and named "Chart 1"
    sheet_name = 'Sheet1'
    chart_name = 'Chart 1'

    # Get a reference to the chart
    chart_sheet = wb.sheets[sheet_name]
    chart = chart_sheet.charts[chart_name]

    # Save and close the workbook
    wb.save()

    # Capture the chart as an image (png format)
    screenshot_path = os.path.abspath('chart_screenshot.png')
    chart.to_png(screenshot_path)

    wb.close()

    # Quit the Excel application
    app.quit()

    # Display the chart using PIL
    img = Image.open(screenshot_path)
    img.show()