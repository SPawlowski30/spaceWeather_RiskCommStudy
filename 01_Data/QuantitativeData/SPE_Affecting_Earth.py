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

split_values = reshaped_df["Flare_Max(UTC)"].str.split("/", n=1, expand=True)
reshaped_df.insert(6, "Flare_Level", split_values[0])
reshaped_df["Flare_Max(UTC)"] = split_values[1]

split_begin_time = reshaped_df["Begin_Time(UTC)"].str.split(" ", n=1, expand=True)
year = split_begin_time[0]  # Extract year
month_day_time = split_begin_time[1].str.split(" ", n=1, expand=True)
month_day = month_day_time[0].str.split("/", expand=True)  # Split month and day
time = month_day_time[1]  # Extract time

# Create new columns
reshaped_df.insert(0, "Day", month_day[1])
reshaped_df.insert(1, "Month", month_day[0])
reshaped_df.insert(2, "Year", year)  #
reshaped_df.insert(3, "Time", time)

#recobine into a new date_number column
reshaped_df["Date_Number"] = (
    reshaped_df["Year"].str.zfill(2) +  #Ensure two-digit day
    reshaped_df["Month"].str.zfill(2) +  #Ensure two-digit month
    reshaped_df["Day"]
)

# Convert Date_Number to integer
reshaped_df["Date_Number"] = reshaped_df["Date_Number"].astype(int)


# Drop the original Begin_Time(UTC) column
reshaped_df.drop(columns=["Begin_Time(UTC)"], errors="ignore", inplace=True)

# Save and print
reshaped_df.to_csv("reformatted_file.csv", index=False)
print(reshaped_df)




