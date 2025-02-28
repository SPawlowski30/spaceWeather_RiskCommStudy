import pandas as pd
import requests
from pathlib import Path

# Load the DataFrame from the previous script
csv_path = Path("/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/TextBasedData/Email_Alerts/NOAA_Alerts/Report_Forecast_Solar_Geophysical_Activity.csv")
df = pd.read_csv(csv_path)

# Output file to store all the combined text
output_filename = "Txt_Report_Forecast_Solar_Geophysical_Activity.txt"

def remove_III(text):
    lines = text.splitlines()
    new_lines = []
    found_III = False

    for line in lines:
        if found_III:
            break
        if line.startswith("III."):
            found_III = True
            continue
        new_lines.append(line)
    return"\n".join(new_lines)

# Open the output file in write mode
with open(output_filename, "w", encoding="utf-8") as outfile:
    for index, row in df.iterrows():
        file_url = row["File Link"]  # Extract the file link

        response = requests.get(file_url)
        response.raise_for_status()  # stops if an error occurs

        lines = response.text.splitlines()
        removed_6 = "\n".join(lines[6:])
        cleaned_text = remove_III(removed_6)

        # Write content to the output file
        outfile.write(cleaned_text +"\n\n")  # Separate files with blank lines


print(f"All files combined into {output_filename}")