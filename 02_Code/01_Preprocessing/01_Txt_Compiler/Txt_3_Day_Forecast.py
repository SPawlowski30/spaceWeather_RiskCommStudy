import pandas as pd
import requests
from pathlib import Path

# Load the DataFrame from the previous script
csv_path = Path("/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/TextBasedData/Email_Alerts/NOAA_Alerts/3_Day_Forecast.csv")
df = pd.read_csv(csv_path)

# Output file to store all the combined text
output_filename = "Txt_3_Day_Forecast.txt"

def is_tab(line):
    words = line.split()
    num_count = sum (1 for word in words if word.replace(".", "",1).isdigit())
    space_count = line.count("  ")
    return num_count > len(words)/2 or space_count >=2

def scrub_a_dub(line):
    unwanted_char = ("A.", "B.", "C.", "Rationale:", ":Product:", ":Issued:")
    for prefix in unwanted_char:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return line

# Open the output file in write mode
with open(output_filename, "w", encoding="utf-8") as outfile:
    for index, row in df.iterrows():
        file_url = row["File Link"]  # Extract the file link

        response = requests.get(file_url)
        response.raise_for_status()  # stops if an error occurs
        text_data = response.text.splitlines()
        cleaned_text_data = [scrub_a_dub(line) for line in text_data if not is_tab(line)]
        # Write content to the output file
        outfile.write("\n".join(cleaned_text_data) + "\n\n")  # Separate files with blank lines
        print(f"Finished processing file {index + 1}")

print(f"All files combined into {output_filename}")
