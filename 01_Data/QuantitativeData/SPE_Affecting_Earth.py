import pandas as pd
import numpy as np

df = pd.read_csv("SPE_Events_NOAA.csv", header=None)

reshaped_array = df.values.flatten().reshape(-1, 10)

custom_headers = ["Begin_Time(UTC)", "Max_Time(UTC)", ">10MeV_Max(pfu)",
                  "Region", "Location", "Flare_Max(UTC)", "Type_II_Radio_Emission",
                  "Type_IV", "Linear_Speed", "Imagery/Misc"]

if len(custom_headers) != reshaped_array.shape[1]:
    raise ValueError("Number of headers must match the number of columns (10).")

reshaped_df = pd.DataFrame(reshaped_array, columns = custom_headers)
reshaped_df.replace(r'^\s*$', np.nan, regex=True, inplace=True)  # Convert empty strings to NaN
reshaped_df.fillna("NA", inplace=True)

#getting flare level
split_values = reshaped_df["Flare_Max(UTC)"].str.split(r"[/\s]", n=1, expand=True)
reshaped_df.insert(6, "Flare_Level", split_values[0])
reshaped_df["Flare_Max(UTC)"] = split_values[1]

#getting event time beginning
split_begin_time = reshaped_df["Begin_Time(UTC)"].str.split(" ", n=1, expand=True)
year = split_begin_time[0]  # Extract year
month_day_time = split_begin_time[1].str.split(" ", n=1, expand=True)
month_day = month_day_time[0].str.split("/", expand=True)  # Split month and day
time = month_day_time[1]  # Extract time

# Create new columns for beginning time
reshaped_df.insert(0, "Begin_Day", month_day[1])
reshaped_df.insert(1, "Begin_Month", month_day[0])
reshaped_df.insert(2, "Begin_Year", year)
reshaped_df.insert(3, "Begin_Time", time)

#recombine into a new beginning date_number column
reshaped_df["Date_Number"] = (
    reshaped_df["Begin_Year"] +  #Ensure two-digit day
    reshaped_df["Begin_Month"].str.zfill(2) +  #Ensure two-digit month
    reshaped_df["Begin_Day"].str.zfill(2)
)

#getting time for max of SPE event
split_max_time = reshaped_df["Max_Time(UTC)"].str.split(" ", n=1, expand=True)
max_year = split_max_time[0]  # Extract year
max_month_day_time = split_max_time[1].str.split(" ", n=1, expand=True)
max_month_day = max_month_day_time[0].str.split("/", expand=True)  # Split month and day
max_time = max_month_day_time[1]  # Extract time

#adding new time columns for max time
reshaped_df.insert(0, "Max_Day", max_month_day[1])
reshaped_df.insert(1, "Max_Month", max_month_day[0])
reshaped_df.insert(2, "Max_Year", max_year)
reshaped_df.insert(3, "Max_Time", max_time)

#recombine into a new max date_number column
reshaped_df["Max_Date_Number"] = (
    reshaped_df["Max_Year"]+
    reshaped_df["Max_Month"].str.zfill(2) +  #Ensure two-digit month
    reshaped_df["Max_Day"].str.zfill(2) +
    reshaped_df["Max_Time"]
)

# Split the Flare_Max(UTC) column
# Extract date and time for rows without a leading string (like "07/28 1558")
flare_without_string = reshaped_df["Flare_Max(UTC)"].str.extract(r'(\d{2}/\d{2})\s*(\d{4})')

# Assign the extracted components to new columns for rows without a leading string
reshaped_df["Flare_Month"] = flare_without_string[0]
reshaped_df["Flare_Time"] = flare_without_string[1]

month_day_split = reshaped_df["Flare_Month"].str.split("/", expand=True)

# Assign the extracted month and day to separate columns
reshaped_df["Flare_Month"] = month_day_split[0]
reshaped_df["Flare_Day"] = month_day_split[1]

reshaped_df["Flare_Date_Number"] = (
    reshaped_df["Begin_Year"] +  # Year from Begin_Year
    reshaped_df["Flare_Month"].str.zfill(2) +  # Ensure two-digit month
    reshaped_df["Flare_Day"].str.zfill(2) +  # Ensure two-digit day
    reshaped_df["Flare_Time"]
)


reshaped_df[">10MeV_Max(pfu)"] = reshaped_df[">10MeV_Max(pfu)"].str.replace(",", "").astype(int)
reshaped_df = reshaped_df.drop(columns=['Region', 'Location', 'Type_II_Radio_Emission', 'Type_IV', 'Linear_Speed', 'Imagery/Misc'])
column_order = [
    "Date_Number",   # Begin_Date_Number comes after
    "Begin_Time(UTC)",
    "Begin_Year",
    "Begin_Month",
    "Begin_Day",
    "Begin_Time",
    "Flare_Date_Number",
    "Flare_Max(UTC)",
    "Flare_Month",
    "Flare_Day",
    "Flare_Time",
    "Max_Date_Number",
    "Max_Time(UTC)",
    "Max_Year",
    "Max_Month",
    "Max_Day",
    "Max_Time",
    "Flare_Level",
    ">10MeV_Max(pfu)"
]
reshaped_df = reshaped_df[column_order]
reshaped_df.to_csv("reformatted_file.csv", index=False)
#print(reshaped_df)




