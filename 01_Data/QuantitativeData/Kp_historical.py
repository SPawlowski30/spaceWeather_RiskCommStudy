import os
import pandas as pd

# Define folder path
folder_path = "../QuantitativeData/Kp_Data"

# List to store extracted data
data_list = []
data_first_three = []

# List all files in the folder
all_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
all_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x.split('Q')[0]))))
# Exclude the first three files

first_three_files = all_files[0:3]
remaining_files = all_files[3:]

#Loop through the files to process
for filename in remaining_files:
    file_path = os.path.join(folder_path, filename)

    # Read file content, starting from line 13
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip lines before line 13 and start parsing from line 13 onwards
    lines_to_process = lines[12:]  # Lines start from line 13 (index 12)

    for line in lines_to_process:
        # Split line by whitespace (or another delimiter, adjust as needed)
        line = line.replace("-", " ")  # Use .split(',') for CSV-like files
        values = line.strip().split()
        # Add 'NA' for any missing values in the line
        row = values + ['NA'] * (30 - len(values))

        # Append the row to the data list
        data_list.append(row)

# Convert list to DataFrame (no column names specified)
df = pd.DataFrame(data_list)
df.drop(df.columns[3:22], axis=1, inplace=True)
custom_headers = ["year", "month", "day", "0000", "0300", "0600", "0900",
                  "1200", "1500", "1800", "2100"]
df.columns = custom_headers

df.replace("NA", pd.NA, inplace=True)  # Convert 'NA' strings to actual missing values (NaN)
df.dropna(how='all', inplace=True)  # Drop rows where all columns are NaN

# Ensure the month and day are two digits
df["month"] = df["month"].astype(str).str.zfill(2)  # Ensure two-digit month format
df["day"] = df["day"].astype(str).str.zfill(2)  # Ensure two-digit day format

# Concatenate day, month (numeric), and year into a single string formatted as ddmmyyyy
df["Date_Number"] = df["year"] + df["month"] + df["day"]

# Optionally, convert to integer if you want Date_Number as a number
df["Date_Number"] = df["Date_Number"].astype(int)


for filename in first_three_files:
    file_path = os.path.join(folder_path, filename)

    # Read file content, starting from line 13
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip lines before line 13 and start parsing from line 13 onwards
    lines_to_process = lines[12:]  # Lines start from line 13 (index 12)

    for line in lines_to_process:
        # Split line by whitespace (or another delimiter, adjust as needed)
        line = line.replace("-", " ")  # Use .split(',') for CSV-like files
        values = line.strip().split()
        # Add 'NA' for any missing values in the line
        row = values + ['NA'] * (30 - len(values))

        # Append the row to the first_three_data_list
        data_first_three.append(row)

# Convert the first three files data into a DataFrame
df_first_three = pd.DataFrame(data_first_three)
df_first_three.drop(df_first_three.columns[3:22], axis=1, inplace=True)

# Set custom headers for the first three files
custom_headers = ["day", "month", "year", "0000", "0300", "0600", "0900",
                  "1200", "1500", "1800", "2100"]
df_first_three.columns = custom_headers

# Replace 'NA' with pd.NA (missing values)
df_first_three.replace("NA", pd.NA, inplace=True)
df_first_three.dropna(how='all', inplace=True)

# Create a dictionary to map month names to month numbers
month_dict = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}

# Apply transformations to the 'month' and 'year' columns
df_first_three["month"] = df_first_three["month"].map(month_dict)

# Add '19' to the 'year' column to make it 4 digits
df_first_three["year"] = "19" + df_first_three["year"].astype(str)

# Ensure the day, month, and year are in the proper format
df_first_three["day"] = df_first_three["day"].astype(str).str.zfill(2)  # Ensure two-digit day format
df_first_three["month"] = df_first_three["month"].astype(str).str.zfill(2)  # Ensure two-digit month format

# Concatenate year, month, and day into a new column 'Date_Number'
df_first_three["Date_Number"] = df_first_three["year"] + df_first_three["month"] + df_first_three["day"]

# Optionally, convert to integer if you want Date_Number as a number
df_first_three["Date_Number"] = df_first_three["Date_Number"].astype(int)
df_first_three = df_first_three[["year", "month", "day"] +
                                [col for col in df_first_three.columns if col not in
                                 ["year", "month", "day"]]]

df_combined = pd.concat([df_first_three, df], ignore_index=True)

# Print the combined DataFrame to check the results
print(df_combined)

# If you want, save the combined DataFrame to a CSV file
output_csv_combined = "kp_output_file.csv"  # Specify the name for the combined CSV file
df_combined.to_csv(output_csv_combined, index=False)
