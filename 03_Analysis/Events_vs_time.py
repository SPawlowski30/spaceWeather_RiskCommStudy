import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt


file_path = "/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/QuantitativeData/merged_df.csv"
df = pd.read_csv(file_path)
#df0 = df.iloc[:140]
df1 = df.iloc[141:232]
df2 = df.iloc[233:275]
df3 = df.iloc[275:]

df1 = df1[df1['Date_Info'].astype(str).str.isnumeric()]
df1['Date_Info']= pd.to_datetime(df1['Date_Info'].astype(str), format='%Y%m%d%H%M', errors='coerce')
df1['Date_Number'] = pd.to_datetime(df1['Date_Number'].astype(str), format='%Y%m%d%H%M')
df1['Time_Difference'] = df1['Date_Number'] - df1['Date_Info']

# Extract days, hours, and minutes separately
df1['Days'] = df1['Time_Difference'].dt.days
df1['Hours'] = df1['Time_Difference'].dt.seconds // 3600
df1['Minutes'] = (df1['Time_Difference'].dt.seconds % 3600) // 60

# Optionally, create a formatted string column
df1['Formatted_Diff'] = df1.apply(lambda x: f"{x['Days']} days {x['Hours']} hrs {x['Minutes']} min", axis=1)

# Display the resulting dataframe
print(df1[['Date_Info', 'Date_Number', 'Days', 'Hours', 'Minutes', 'Formatted_Diff']])



"""
df2 = df2[df2['Date_Info'].astype(str).str.isnumeric()]
df2['Date_Info']= pd.to_datetime(df2['Date_Info'].astype(str), format='%Y%m%d%H%M', errors='coerce')
df2['Date_Number'] = pd.to_datetime(df2['Date_Number'].astype(str), format='%Y%m%d%H%M')

df3 = df3[df3['Date_Info'].astype(str).str.isnumeric()]
df3['Date_Info']= pd.to_datetime(df3['Date_Info'].astype(str), format='%Y%m%d%H%M', errors='coerce')
df3['Date_Number'] = pd.to_datetime(df3['Date_Number'].astype(str), format='%Y%m%d%H%M')

plt.figure(figsize=(10, 6))
plt.scatter(df1['Date_Info'], df1['Flare_Class'], label='Flares', color='red', alpha=0.5)
plt.scatter(df1['Date_Number'], df1['Proton_class'], label='SEP event', color='green', alpha=0.5)
plt.scatter(df1['Date_Number'], df1['Kp_Class'], label='Kp_index', color='blue', alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Index')
plt.title('Three Space Weather Warning Metrics vs. Time (1994-2008)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Create the second plot for df2 (233-275 rows)
plt.figure(figsize=(10, 6))
plt.scatter(df2['Date_Info'], df2['Flare_Class'], label='Flares', color='red', alpha=0.5)
plt.scatter(df2['Date_Number'], df2['Proton_class'], label='SEP event', color='blue', alpha=0.5)
plt.scatter(df2['Date_Number'], df2['Kp_Class'], label='Kp_index', color='green', alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Index')
plt.title('Three Space Weather Warning Metrics vs. Time (2008-2019)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Create the third plot for df3 (275 and onwards)
plt.figure(figsize=(10, 6))
plt.scatter(df3['Date_Info'], df3['Flare_Class'], label='Flares', color='red', alpha=0.5)
plt.scatter(df3['Date_Number'], df3['Proton_class'], label='SEP event', color='blue', alpha=0.5)
plt.scatter(df3['Date_Number'], df3['Kp_Class'], label='Kp_index', color='green', alpha=0.5)
plt.xlabel('Year')
plt.ylabel('Index')
plt.title('Three Space Weather Warning Metrics vs. Time (2008-2019)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
"""