#prop = {"size": 24},
#title_fontsize = 24)
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path2 = "../02_Code/04_Quantitative/Outputs/max_merged_df.csv"
file_path = "../02_Code/04_Quantitative/Outputs/begin_merged_df.csv"
df = pd.read_csv(file_path) # begin
df2 = pd.read_csv(file_path2) # max
print(df.head())

df_subset = df.iloc[141:]
df_subset2 = df2.iloc[141:]

k_index_values = df_subset['Kp_Class']
k_index_values_2 = df_subset2['Kp_Class']

bins = np.arange(0, 7)
counts, bin_edges = np.histogram(k_index_values, bins=bins)

#Proton_Class
proton_class_values = df['Proton_class']
counts, bin_edges = np.histogram(proton_class_values, bins=bins)

#Flare_class
flare_class_values = df['Flare_Class']
counts, bin_edges = np.histogram(flare_class_values, bins=bins)



color_map = {
    0: '#92d051', #light green
    1: '#f6eb13', #yellow
    2: '#ffc800', #light orange
    3: '#ff9600', #dark orange
    4: '#ff0000', #red
    5: '#c70100'  #dark red
}
fig, axs = plt.subplots(1, 3, figsize=(18, 6))  # Horizontal layout

# ----------------------
# First pie: Kp Index
# ----------------------
kp_counts = k_index_values_2.value_counts().sort_index()
labels_kp = kp_counts.index
sizes_kp = kp_counts.values
colors_kp = [color_map[label] for label in labels_kp]

wedges_kp, _ = axs[2].pie(
    sizes_kp,
    labels=None,
    colors=colors_kp,
    startangle=140,
    wedgeprops={'edgecolor': 'white'}
)
axs[2].set_title('G', fontsize=24)

# ----------------------
# Second pie: Flare Class
# ----------------------
flare_counts = flare_class_values.value_counts().sort_index()
labels_flare = flare_counts.index
sizes_flare = flare_counts.values
colors_flare = [color_map[label] for label in labels_flare]

wedges_flare, _ = axs[0].pie(
    sizes_flare,
    labels=None,
    colors=colors_flare,
    startangle=140,
    wedgeprops={'edgecolor': 'white'}
)
axs[0].set_title('R', fontsize=24)

# ----------------------
# Third pie: Proton Event
# ----------------------
proton_counts = proton_class_values.value_counts().sort_index()
labels_proton = proton_counts.index
sizes_proton = proton_counts.values
colors_proton = [color_map[label] for label in labels_proton]

wedges_proton, _ = axs[1].pie(
    sizes_proton,
    labels=None,
    colors=colors_proton,
    startangle=140,
    wedgeprops={'edgecolor': 'white'}
)
axs[1].set_title('S', fontsize=24)

# ----------------------
# Shared Legend
# ----------------------
all_labels = sorted(set(labels_kp) | set(labels_flare) | set(labels_proton))
legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w',
               label=label,
               markerfacecolor=color_map[label],
               markeredgecolor='white',
               markersize=24)
    for label in all_labels
]

# Add legend to the figure (not to an axis!)
fig.legend(
    handles=legend_handles,
    labels=all_labels,
    loc='lower center',
    ncol=len(all_labels),
    title="Warning Levels",
    title_fontsize=24,
    prop={'size': 18},
    bbox_to_anchor=(0.5, 0.1)
)

# Adjust layout to make room for legend
plt.subplots_adjust(bottom=0.2, top=0.88)
plt.show()

fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

bins = np.arange(0, 7)

# ----------------------
# (R) Flare Class
# ----------------------
counts, bin_edges = np.histogram(flare_class_values, bins=bins)
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
axs[0].bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
axs[0].set_xticks(bar_centers)
axs[0].set_xticklabels(np.arange(0, 6))
axs[0].set_xlabel('Level')
axs[0].set_ylabel('Count')
axs[0].set_title('R', fontsize=24)

# ----------------------
# (S) Proton Class
# ----------------------
counts, bin_edges = np.histogram(proton_class_values, bins=bins)
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
axs[1].bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
axs[1].set_xticks(bar_centers)
axs[1].set_xticklabels(np.arange(0, 6))
axs[1].set_xlabel('Level')
axs[1].set_title('S', fontsize=24)

# ----------------------
# (G) Kp Index
# ----------------------
counts, bin_edges = np.histogram(k_index_values_2, bins=bins)
colors = [color_map.get(int(bin_edges[i]), 'gray') for i in range(len(bin_edges) - 1)]
bar_centers = bin_edges[:-1] + 0.5
axs[2].bar(bin_edges[:-1], counts, width=np.diff(bin_edges), color=colors, edgecolor='black', align='edge')
axs[2].set_xticks(bar_centers)
axs[2].set_xticklabels(np.arange(0, 6))
axs[2].set_xlabel('Level')
axs[2].set_title('G', fontsize=24)

# ----------------------
# Adjust layout
# ----------------------
plt.tight_layout(rect=[0, 0, 1, 0.92])  # Leave space for suptitle
plt.show()

fig, axs = plt.subplots(2, 3, figsize=(18, 10))  # 2 rows: top pies, bottom bars
#-------COMBINED GRAPHS-----------
# === PIE CHARTS (Top row) ===
# -------- R: Flare Class --------
flare_counts = flare_class_values.value_counts().sort_index()
labels_flare = flare_counts.index
sizes_flare = flare_counts.values
colors_flare = [color_map[label] for label in labels_flare]
axs[0, 0].pie(
    sizes_flare,
    labels=[f'{s / sum(sizes_flare) * 100:.1f}%' for s in sizes_flare],
    colors=colors_flare,
    startangle=140,
    wedgeprops={'edgecolor': 'white'},
    textprops={'fontsize': 11}
)
axs[0, 0].set_title('R', fontsize=24)

# -------- S: Proton Class --------
proton_counts = proton_class_values.value_counts().sort_index()
labels_proton = proton_counts.index
sizes_proton = proton_counts.values
colors_proton = [color_map[label] for label in labels_proton]
axs[0, 1].pie(
    sizes_proton,
    labels=[f'{s / sum(sizes_proton) * 100:.1f}%' for s in sizes_proton],
    colors=colors_proton,
    startangle=140,
    wedgeprops={'edgecolor': 'white'},
    textprops={'fontsize': 11}
)
axs[0, 1].set_title('S', fontsize=24)

# -------- G: Kp Index --------
kp_counts = k_index_values_2.value_counts().sort_index()
labels_kp = kp_counts.index
sizes_kp = kp_counts.values
colors_kp = [color_map[label] for label in labels_kp]
axs[0, 2].pie(
    sizes_kp,
    colors=colors_kp,
    startangle=140,
    wedgeprops={'edgecolor': 'white'}

)
axs[0, 2].set_title('G', fontsize=24)

# === BAR GRAPHS (Bottom row) ===
bins = np.arange(0, 7)
bar_labels = np.arange(0, 6)

# -------- R: Flare Class --------
counts, bin_edges = np.histogram(flare_class_values, bins=bins)
colors = [color_map.get(i, 'gray') for i in bar_labels]
axs[1, 0].bar(bar_labels, counts, color=colors, edgecolor='white', width = 1.0)
axs[1, 0].set_xticks(bar_labels)
axs[1, 0].set_xlabel('Level', fontsize=14)
axs[1, 0].set_ylabel('Count', fontsize=14)
axs[1, 0].tick_params(axis='both', labelsize=12)


# -------- S: Proton Class --------
counts, bin_edges = np.histogram(proton_class_values, bins=bins)
axs[1, 1].bar(bar_labels, counts, color=colors, edgecolor='white', width = 1.0)
axs[1, 1].set_xticks(bar_labels)
axs[1, 1].set_xlabel('Level', fontsize=14)
axs[1, 1].tick_params(axis='both', labelsize=12)


# -------- G: Kp Index --------
counts, bin_edges = np.histogram(k_index_values_2, bins=bins)
axs[1, 2].bar(bar_labels, counts, color=colors, edgecolor='white', width = 1.0)
axs[1, 2].set_xticks(bar_labels)
axs[1, 2].set_xlabel('Level', fontsize=14)
axs[1, 2].tick_params(axis='both', labelsize=12)


# === SHARED LEGEND ===
all_labels = sorted(set(labels_kp) | set(labels_flare) | set(labels_proton))
legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w',
               label=label,
               markerfacecolor=color_map[label],
               markeredgecolor='white',
               markersize=14)
    for label in all_labels
]
fig.legend(
    handles=legend_handles,
    labels=all_labels,
    loc='lower center',
    ncol=len(all_labels),
    title="Warning Levels",
    title_fontsize=14,
    prop={'size': 10},
    bbox_to_anchor=(0.5, -0.01)  # Lower the legend further
)

plt.tight_layout(rect=[0, 0.07, 1, 0.93])  # Leave extra space below for legend
plt.show()
"""
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


#Pie_plot kp_index_max
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

fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
"""
