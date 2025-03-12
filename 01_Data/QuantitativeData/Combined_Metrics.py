import pandas as pd

df1 = pd.read_csv('reformatted_file.csv')
df2 = pd.read_csv('kp_output_file.csv')
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


"""
df["Time"] = df["Time"].astype(str).str.strip().str.zfill(4)
df["Date_Number"] = df["Date_Number"].astype(str) + df["Time"]

columns_to_check = ["0000", "0300", "0600", "0900", "1200", "1500", "1800", "2100"]
df[columns_to_check] = df[columns_to_check].apply(pd.to_numeric, errors='coerce')
df["Kp_Sum"] = df[columns_to_check].sum(axis=1)

# Apply classification based on the sum
df["Kp_Class"] = df["Kp_Sum"].apply(
    lambda x: 0 if 0 <= x < 5 else
              (1 if x < 6 else
               (2 if x < 7 else
                (3 if x < 8 else
                 (4 if x < 9 else
                  (5 if x == 9 else None)))))
)

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
df['Flare_Class'] = df['Flare_Level'].apply(flare_class)

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
df['Proton_class'] = df['>10MeV_Max(pfu)'].apply(proton_class)


"""
# Save the modified dataframe to a new CSV file
df_Max.to_csv('max_merged_df.csv', index=False)
df_Begin.to_csv('begin_merged_df.csv', index=False)
#print(df.columns)


# Display the updated dataframe
#print(df)

