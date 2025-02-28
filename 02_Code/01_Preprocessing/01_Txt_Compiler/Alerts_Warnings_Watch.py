"""This scripts takes JSON data that contains Alerts, Warnings, and Watches from 01/27/25 - 02/25/25 it
 filters out duplicates and returns the unique entries in a txt file"""

import requests
import json

json_url = "https://services.swpc.noaa.gov/products/alerts.json"

# Fetch the JSON data
response = requests.get(json_url)

if response.status_code == 200:
        json_data = response.json()  #Parse JSON content

        #filter to unique alerts
        unique_alerts = {}
        for alert in json_data:
            product_id = alert.get("product_id")
            if product_id not in unique_alerts:
                unique_alerts[product_id] = [alert]
        unique_alerts_list = list(unique_alerts.values())
        print("total number of unique alerts: " + str(len(unique_alerts_list)))

        #save to a txt file
        output_file = "Txt_Alerts_Warnings_Watch.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            for alert in unique_alerts_list:
                alert_text = json.dumps(alert, indent = 4)
                clean_text = "\n".join(
                    line for line in alert_text.split("\n")
                    if '"product_id"' not in line and '"issue_datetime"' not in line)
                f.write(clean_text+ "\n\n")
        print("txt file saved successfully")
else:
    print(f"Error: Failed to fetch JSON. HTTP Status Code: {response.status_code}")