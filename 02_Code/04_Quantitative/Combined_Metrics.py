import pandas as pd

"""
This script merges the historic k-index data with the SPE event data, it creates two csvs. One with k-index
aligned with the beginning of the SPE event data, the other aligned with the max SPE event data.
"""

df1 = pd.read_csv('Outputs/reformatted_file.csv')
df2 = pd.read_csv('Outputs/kp_output_file.csv')
df2 = df2.iloc[:, 3:]
# Merge the two dataframes on the "Date_Number" column
merged_df = pd.merge(df1, df2, on="Date_Number", how="left")

def adjust_time_columns(row, time_columns, time_column_name):
    time_str = row[time_column_name]
    if pd.isna(time_str):
        return row

    current_time = int(time_str)

    # Find the closest time match
    closest_time = None
    for col in time_columns:
        col_time = int(col)  # Convert column header to integer (e.g., '1200' -> 1200)
        if current_time >= col_time:
            closest_time = col_time
        else:
            break

    # Set the appropriate column to the original value and the others to 0
    for col in time_columns:
        if col == str(closest_time).zfill(4):  # If this is the closest time, keep the original value
            row[col] = row[col] if pd.notna(row[col]) else 0 # Leave the value unchanged
        else:  # Set all other columns to 0
            row[col] = 0

    return row

# Apply the function to each row in the dataframe
time_columns = ['0000', '0300', '0600', '0900', '1200', '1500', '1800', '2100']
df_Begin = merged_df.apply(adjust_time_columns, axis=1, time_columns=time_columns, time_column_name='Begin_Time')
df_Max = merged_df.apply(adjust_time_columns, axis=1, time_columns=time_columns, time_column_name='Max_Time')
print(df_Begin)
print(df_Max)

#df_Max["Flare_Date_Number"] = df_Max["Flare_Date_Number"].astype(int)
#df_Begin["Flare_Date_Number"] = df_Begin["Flare_Date_Number"].astype(int)
#df_Max["Max_Date_Number"] = df_Max["Max_Date_Number"].astype(int)
#df_Begin["Flare_Date_Number"] = df_Begin["Flare_Date_Number"].astype(int)
# Ensure Begin_Time is a string before applying str.zfill

#The code in between the #-------# are the functions used to compute the warning levels
#----------------------------------------------------------------------------------------------#
# for finding G warning level applies to k-index
def classify_kp(df, columns_to_check): #This will have to be handled slightly differently on dashboard

    # Convert columns to numeric, coercing errors to NaN
    df[columns_to_check] = df[columns_to_check].apply(pd.to_numeric, errors='coerce')

    # Compute the sum
    df["Kp_Sum"] = df[columns_to_check].sum(axis=1) #no need to sum for dashboard, this is a product of how the csv was organized

    # Apply classification based on the sum
    def kp_classification(x):
        if 0 <= x < 5:
            return 0
        elif x < 6:
            return 1
        elif x < 7:
            return 2
        elif x < 8:
            return 3
        elif x < 9:
            return 4
        elif x == 9:
            return 5
        return None  # Handle cases where x is NaN or outside expected range

    df["Kp_Class"] = df["Kp_Sum"].apply(kp_classification)

    return df

columns_to_check = ["0000", "0300", "0600", "0900", "1200", "1500", "1800", "2100"]

df_Max = classify_kp(df_Max, columns_to_check)
df_Begin = classify_kp(df_Begin, columns_to_check)

#R warning applied to flare levels, this strategy will not work for dashboard, need to use numeric thresholds instead
def flare_class(level):
    # Ensure the value is a string before applying string methods
    if isinstance(level, str):
        if level.startswith("C"):
            return 0  # If flare starts with "C", return 0
        # Check if the level starts with 'M'
        if level.startswith("M"):
            number_part = level[1:]
            try:
                number = float(number_part)  # Try to convert the rest to a float
                if 1 <= number < 5:
                    return 1
                elif number >= 5:
                    return 2
            except ValueError:
                return None  #If the number can't be converted

        # Check if the level starts with 'X'
        elif level.startswith("X"):
            number_part = level[1:]
            try:
                number = float(number_part)  # Try to convert the rest to a float
                if 1 <= number < 10:
                    return 3
                elif 10 <= number < 20:
                    return 4
                elif number >= 20:
                    return 5
            except ValueError:
                return None  #If the number can't be converted
        # If the string doesn't start with 'M' or 'X', return None
        return None

    return None

# Apply the function to the Flare_Level column to create the Flare_Class column
df_Max['Flare_Class'] = df_Max['Flare_Level'].apply(flare_class)
df_Begin['Flare_Class'] = df_Begin['Flare_Level'].apply(flare_class)

#For R warning, use this one for the real time data
def flare_class_numeric(value):
    if isinstance(value, (int, float)):
        if (10**-5) <= value < 5*(10**-5):
            return 1
        elif 5*(10**-5) <= value < (10**-4):
            return 2
        elif (10**-4) <= value < (10**-3):
            return 3
        elif (10**-3) <= value < (2*(10**-3)):
            return 4
        elif value>= (2*(10**-3)):
            return 5
    return None

#S warnings applies to proton data, should work the exact same on dashboard
def proton_class(value):
    # Check if the value is an integer or float and handle it appropriately
    if isinstance(value, (int, float)):
        if 10 < value < 100:
            return 1
        elif 100 <= value < 1000:
            return 2
        elif 1000 <= value < 10000:
            return 3
        elif 10000 <= value < 100000:
            return 4
        elif value >= 100000:
            return 5
    return None
#-------------------------------------------------------------------------------------------------#
df_Max['Proton_class'] = df_Max['>10MeV_Max(pfu)'].apply(proton_class)
df_Begin['Proton_class'] = df_Begin['>10MeV_Max(pfu)'].apply(proton_class)

df_Max["Begin_Time"] = df_Max["Begin_Time"].astype(str)
df_Begin["Begin_Time"] = df_Begin["Begin_Time"].astype(str)
df_Max["Date_Number"] = df_Max["Date_Number"].astype(str)
df_Begin["Date_Number"] = df_Begin["Date_Number"].astype(str)
df_Max["Begin_Date_Number"] = df_Max["Date_Number"] + df_Max["Begin_Time"].str.zfill(4)
df_Begin["Begin_Date_Number"] = df_Begin["Date_Number"] + df_Begin["Begin_Time"].str.zfill(4)
df_Max["Begin_Date_Number"] = df_Max["Begin_Date_Number"].astype(int)
df_Begin["Begin_Date_Number"] = df_Begin["Begin_Date_Number"].astype(int)
df_Max.insert(1, "Begin_Date_Number", df_Max.pop("Begin_Date_Number"))
df_Begin.insert(1, "Begin_Date_Number", df_Begin.pop("Begin_Date_Number"))

df_Max.to_csv('max_merged_df.csv', index=False)
df_Begin.to_csv('begin_merged_df.csv', index=False)


