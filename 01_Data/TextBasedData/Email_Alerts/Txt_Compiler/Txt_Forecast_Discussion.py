import pandas as pd
import requests
from pathlib import Path

# Load the DataFrame from the previous script
csv_path = Path("/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/TextBasedData/Email_Alerts/NOAA_Alerts/Forecast_Discussion.csv")
df = pd.read_csv(csv_path)

# Output file to store all the combined text
output_filename = "Txt_Forecast_Discussion.txt"

# Open the output file in write mode
with open(output_filename, "w", encoding="utf-8") as outfile:
    for index, row in df.iterrows():
        file_url = row["File Link"]  # Extract the file link

        response = requests.get(file_url)
        response.raise_for_status()  # stops if an error occurs

        # Write content to the output file
        outfile.write(response.text)
        outfile.write("\n\n")  # Separate files with blank lines


print(f"All files combined into {output_filename}")