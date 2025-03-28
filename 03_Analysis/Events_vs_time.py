import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_path = ("../01_Data/QuantitativeData/max_merged_df.csv")

df = pd.read_csv(file_path)


def convert_to_datetime(df, column):
    df_copy = df.copy()
    df_copy = df_copy.dropna(subset=[column])
    df_copy[column] = df_copy[column].astype(float).astype(int)

    # Convert the integers to datetime format (YYYYMMDDHHMM)
    df_copy[column] = pd.to_datetime(df_copy[column].astype(str), format='%Y%m%d%H%M', errors='coerce')
    return df_copy

df_copy = convert_to_datetime(df, "Flare_Date_Number")
df_copy = convert_to_datetime(df_copy, "Begin_Date_Number")
df_copy = convert_to_datetime(df_copy, "Max_Date_Number")

# Check the converted columns
print(df_copy[['Flare_Date_Number', 'Begin_Date_Number']].head())


def subtract_as_integers(df, column1, column2):
    df_copy = df.copy()
    df_copy = df_copy.dropna(subset=[column1, column2])
    time_diff = df_copy[column1] - df_copy[column2]

    # Calculate days, hours, and minutes
    df_copy['Days'] = time_diff.dt.days
    df_copy['Hours'] = time_diff.dt.seconds // 3600
    df_copy['Minutes'] = (time_diff.dt.seconds % 3600) // 60

    # Combine the time difference into a single column in minutes
    df_copy['TotalMinutes'] = df_copy['Days'] * 1440 + df_copy['Hours'] * 60 + df_copy['Minutes']

    # Print the results
    print("\nTime differences (in days, hours, and minutes) between 'Flare_Date_Number' and 'Begin_Date_Number':")
    print(df_copy[['Flare_Date_Number', 'Begin_Date_Number', 'Days', 'Hours', 'Minutes', 'TotalMinutes']])

    return df_copy


# Perform the subtraction and calculate the total time difference in minutes
df_copy = subtract_as_integers(df_copy, "Begin_Date_Number", "Flare_Date_Number")

min_time = -5760
max_time = 5760

filtered_data = df_copy['TotalMinutes'].dropna()
filtered_data = filtered_data[(filtered_data >= min_time) & (filtered_data <= max_time)]

plt.figure(figsize=(10, 6))
plt.hist(filtered_data, bins=30, color='skyblue', edgecolor='black')

# Set the x-axis limits to match the filtered range
plt.xlim(min_time, max_time)
plt.yscale('log')
plt.title("Histogram of Time Differences in Minutes(±3 Days)")
plt.xlabel("Time Difference (in minutes)")
plt.ylabel("Frequency (log scale)")
plt.grid(True)
plt.show()

df_copy = subtract_as_integers(df_copy, "Max_Date_Number", "Flare_Date_Number")

min_time = 0
max_time = 8640

filtered_data = df_copy['TotalMinutes'].dropna()
filtered_data = filtered_data[(filtered_data >= min_time) & (filtered_data <= max_time)]

plt.figure(figsize=(10, 6))
plt.hist(filtered_data, bins=30, color='#b53158', edgecolor='white')

# Set the x-axis limits to match the filtered range
plt.xlim(min_time, max_time)
plt.yscale('log')

minutes_in_day = 1440
ticks = np.arange(min_time // minutes_in_day * minutes_in_day, max_time, minutes_in_day)

# Add custom tick marks and labels
plt.xticks(ticks, [f"Day {i}" for i in range(len(ticks))])

plt.title("Time Differences in Days Between Solar Flare and Maximum of SPE")
plt.xlabel("Time Difference")
plt.ylabel("Frequency (log scale)")
plt.grid(True)
plt.show()

df_copy = subtract_as_integers(df_copy, "Max_Date_Number", "Begin_Date_Number")

min_time = -5760
max_time = 5760

filtered_data = df_copy['TotalMinutes'].dropna()
filtered_data = filtered_data[(filtered_data >= min_time) & (filtered_data <= max_time)]

plt.figure(figsize=(10, 6))
plt.hist(filtered_data, bins=30, color='skyblue', edgecolor='black')

# Set the x-axis limits to match the filtered range
plt.xlim(min_time, max_time)
plt.yscale('log')
plt.title("Histogram of Time Differences in Minutes(±3 Days)")
plt.xlabel("Time Difference (in minutes)")
plt.ylabel("Frequency (log scale)")
plt.grid(True)
plt.show()