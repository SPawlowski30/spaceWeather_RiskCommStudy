import pandas as pd

df1 = pd.read_csv('reformatted_file.csv')  # Replace with your actual file paths
df2 = pd.read_csv('kp_output_file.csv')
df2 = df2.iloc[:, 3:]
# Merge the two dataframes on the "Date_Number" column
merged_df = pd.merge(df1, df2, on="Date_Number", how="left")
merged_df.to_csv("merged_df.csv", index=False)

# Display the merged dataframe
print(merged_df)

