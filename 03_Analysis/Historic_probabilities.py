import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path2 = "/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/QuantitativeData/max_merged_df.csv"
file_path = "/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/QuantitativeData/begin_merged_df.csv"
df = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)
print(df.head())

df_subset = df.iloc[141:]
df_subset2 = df2.iloc[141:]

k_index_values = df_subset['Kp_Class']
k_index_values_2 = df_subset2['Kp_Class']

bins = np.arange(0, 7)
counts, bin_edges = np.histogram(k_index_values, bins=bins)

color_map = {
    0: '#92d051', #light green
    1: '#f6eb13', #yellow
    2: '#ffc800', #light orange
    3: '#ff9600', #dark orange
    4: '#ff0000', #red
    5: '#c70100'  #dark red
}

#Bar graph kp_index_begin
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
plt.bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
plt.xticks(bar_centers, labels=np.arange(0, 6))

plt.xlabel('Level 0-5')
plt.ylabel('Count')
plt.suptitle('(G) Geomagnetic Storm Warning Bar Graph')
plt.title("1994 - Present Day, Level Associated with Beginning of Proton Event")
plt.show()

#Pie_plot kp_index_begin
kp_counts = k_index_values.value_counts().sort_index()
labels = kp_counts.index
sizes = kp_counts.values
colors = [color_map[label] for label in labels]

plt.figure(figsize=(8, 9))
wedges, texts = plt.pie(sizes, labels=labels, colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'}, labeldistance=1.2)

percentages = [f'{size / sum(sizes) * 100:.1f}%' for size in sizes]
plt.legend(wedges, [f'{label}: {perc}' for label, perc in zip(labels, percentages)], title="Kp Class", loc="center left", bbox_to_anchor=(0.95, 0.5))
plt.suptitle('(G) Geomagnetic Storm Warning Level Proportions')
plt.title("Level Associated with Beginning of Proton Event")
plt.show()

#Bar graph kp_index_max
counts, bin_edges = np.histogram(k_index_values_2, bins=bins)
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
plt.bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
plt.xticks(bar_centers, labels=np.arange(0, 6))

plt.xlabel('Level 0-5')
plt.ylabel('Count')
plt.suptitle('(G) Geomagnetic Storm Warning Bar Graph')
plt.title("1994 - Present Day, Level Associated with Maximum of Proton Event")
plt.show()

#Pie_plot kp_index_begin
kp_counts = k_index_values_2.value_counts().sort_index()
labels = kp_counts.index
sizes = kp_counts.values
colors = [color_map[label] for label in labels]

plt.figure(figsize=(8, 9))
wedges, texts = plt.pie(sizes, labels=labels, colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'}, labeldistance=1.2)

percentages = [f'{size / sum(sizes) * 100:.1f}%' for size in sizes]
plt.legend(wedges, [f'{label}: {perc}' for label, perc in zip(labels, percentages)], title="Kp Class", loc="center left", bbox_to_anchor=(0.95, 0.5))
plt.suptitle('Geomagnetic Storm Warning Level Proportions')
plt.title("Level Associated with Maximum of Proton Event")
plt.show()

#Flare_class
flare_class_values = df['Flare_Class']
counts, bin_edges = np.histogram(flare_class_values, bins=bins)

#Bar graph Flare_class
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
plt.bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
plt.xticks(bar_centers, labels=np.arange(0, 6))

plt.xlabel('Level 0-5')
plt.ylabel('Count')
plt.suptitle('(R) Radio Blackout Warning Bar Graph')
plt.title("1976 - Present Day")
plt.show()


#Pie_plot Flare_class
flare_counts = flare_class_values.value_counts().sort_index()
labels = flare_counts.index
sizes = flare_counts.values
colors = [color_map[label] for label in labels]

plt.figure(figsize=(8, 9))
wedges, texts = plt.pie(sizes, labels=labels, colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'}, labeldistance=1.2)

percentages = [f'{size / sum(sizes) * 100:.1f}%' for size in sizes]
plt.legend(wedges, [f'{label}: {perc}' for label, perc in zip(labels, percentages)], title="Flare Class", loc="center left", bbox_to_anchor=(0.93, 0.5))
plt.title('(R) Radio Blackout Warning Level Proportions')
plt.show()

#Proton_Class
proton_class_values = df['Proton_class']
counts, bin_edges = np.histogram(proton_class_values, bins=bins)

#Bar graph Proton_Class
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
plt.bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
plt.xticks(bar_centers, labels=np.arange(0, 6))

plt.xlabel('Level 0-5')
plt.ylabel('Count')
plt.suptitle('(S) Solar Radiation Storm Warning Bar Graph')
plt.title("1976 - Present Day")
plt.show()

#Pie_plot Proton_class
proton_counts = proton_class_values.value_counts().sort_index()
labels = proton_counts.index
sizes = proton_counts.values
colors = [color_map[label] for label in labels]

plt.figure(figsize=(8, 9))
wedges, texts = plt.pie(sizes, labels=labels, colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'}, labeldistance=1.2)

percentages = [f'{size / sum(sizes) * 100:.1f}%' for size in sizes]
plt.legend(wedges, [f'{label}: {perc}' for label, perc in zip(labels, percentages)], title="Flare Class", loc="center left", bbox_to_anchor=(0.93, 0.5))
plt.title('(S) Solar Radiation Storm Warning Level Proportions')
plt.show()

max_value = df["Flare_Class"].max()
print(max_value)
max_index = df["Flare_Class"].idxmax()
print(max_index)
