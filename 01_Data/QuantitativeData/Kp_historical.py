import os
import pandas as pd

# Define folder path
folder_path = "/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/QuantitativeData/Kp_Data"

# List to store extracted data
data_list = []

# List all files in the folder
all_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
all_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split('Q')[0]))))
# Exclude the first three files
files_to_process = all_files[3:]

#Loop through the files to process
for filename in files_to_process:
    file_path = os.path.join(folder_path, filename)

    # Read file content, starting from line 13
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip lines before line 13 and start parsing from line 13 onwards
    lines_to_process = lines[12:]  # Lines start from line 13 (index 12)

    for line in lines_to_process:
        # Split line by whitespace (or another delimiter, adjust as needed)
        values = line.strip().split()  # Use .split(',') for CSV-like files

        # Add 'NA' for any missing values in the line
        row = values + ['NA'] * (35 - len(values))

        # Append the row to the data list
        data_list.append(row)

# Convert list to DataFrame (no column names specified)
df = pd.DataFrame(data_list)

# Display the DataFrame
print(df)
output_csv = "kp_output_file.csv"  # Specify the name for the CSV file
df.to_csv(output_csv, index=False)