import requests
import json

# NOAA Alerts JSON URL from 02/24/25 - 01/27/25
json_url = "https://services.swpc.noaa.gov/products/alerts.json"

# Fetch the JSON data
response = requests.get(json_url)

# Check if the request was successful
if response.status_code == 200:
        json_data = response.json()  # Parse JSON content
        print(json.dumps(json_data, indent=4))  # Pretty-print full JSON
else:
    print(f"Error: Failed to fetch JSON. HTTP Status Code: {response.status_code}")