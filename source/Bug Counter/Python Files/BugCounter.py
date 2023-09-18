import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

def count_bugs():
    product = product_entry.get()
    component = component_entry.get()
    severity = severity_entry.get()
    date = date_entry.get()

    # Base URL and api key used to access TMEIC Bugzilla materials handling database
    base_url = "https://tools.tmeic.com/mh/rest/bug"
    api_key = "JrfGl8dx6tbK331csReq63YrP02yQ0PFUKceJUtS"  # this was my (Daniel Byrnes, intern) API key generated from my MH Bugzilla account

    url_noDate = f"{base_url}?product={product}&component={component}&severity={severity}&api_key={api_key}"
    url_Date = f"{base_url}?product={product}&component={component}&severity={severity}&creation_time={date}&api_key={api_key}"

    if not (date and date.strip()):
        url = url_noDate
    else:
        url = url_Date

    # Fetch .json of severe bugs from bugzilla
    response = requests.get(url)
    data = response.json()

    # Initialize a counter for closed bugs
    open_count = 0
    closed_count = 0
    # Iterate through the list of bugs and count closed bugs
    for bug in data["bugs"]:
        if bug["is_open"]:
            open_count += 1
        else:
            closed_count +=1

    # Display the result
    result_label.config(text=f"\nThe number of bugs for\n\nproduct: {product}\nseverity: {severity}\nsince date: {date}\n\nis:\n{open_count} open bugs,\n{closed_count} closed bugs")

# Create the main application window
root = tk.Tk()
root.title("Bugzilla Bug Counter")

# Set the initial size of the window
window_width = 500  # You can adjust this value as needed
window_height = 400  # You can adjust this value as needed
root.geometry(f"{window_width}x{window_height}")

# Create and place input fields and labels
product_label = ttk.Label(root, text="Enter the product (project):")
product_label.pack()
product_entry = ttk.Entry(root)
product_entry.pack()

component_label = ttk.Label(root, text="Enter the component:")
component_label.pack()
component_entry = ttk.Entry(root)
component_entry.pack()

severity_label = ttk.Label(root, text="Enter the bug severity:")
severity_label.pack()
severity_entry = ttk.Entry(root)
severity_entry.pack()

date_label = ttk.Label(root, text="Enter the date created (yyyy-mm-dd):")
date_label.pack()
date_entry = ttk.Entry(root)
date_entry.pack()

# Create and place the "Count Bugs" button
count_button = ttk.Button(root, text="Count Bugs", command=count_bugs)
count_button.pack()

# Create and place the label to display the result
result_label = ttk.Label(root, text="")
result_label.pack()

# Start the main event loop
root.mainloop()