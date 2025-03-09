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
reshaped_df.insert(6, "Flare_Level", split_values[0])  # Insert as the 7th column
reshaped_df["Flare_Max(UTC)"] = split_values[1]

#reshaped_df.to_csv("reformatted_file.csv", index=False, header=False)
reshaped_df.to_csv("reformatted_file.csv", index=False)
print(reshaped_df)