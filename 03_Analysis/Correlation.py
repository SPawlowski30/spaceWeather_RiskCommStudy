import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


file_path = "../02_Code/05_Quantitative/Outputs/max_merged_df.csv"
df = pd.read_csv(file_path)

#columns of interest
df_corr = df[['Proton_class', 'Flare_Class', 'Kp_Class']]
labels = ['S Level', 'R Level', 'G Level']


df_corr = df_corr.dropna()

# Compute correlation matrix
corr = df_corr.corr()

# Create a custom colormap:
colors = ["#e98d6b", "#df8090", "#6c2b6d"]  # purple → peach → pink
custom_cmap = LinearSegmentedColormap.from_list("spaceweather", colors)


plt.figure(figsize=(8, 6))
sns.heatmap(
    corr,
    annot=True,
    fmt=".4f",  # Four decimal places
    annot_kws={"size": 10},
    cmap=custom_cmap,
    vmin=-1,
    vmax=1,
    center=0,
    linewidths=0.5,
    linecolor='gray',
    xticklabels=labels,
    yticklabels=labels
)

plt.title("Correlation Matrix of Space Weather Warning Metrics", fontsize=14, pad=12)
plt.tight_layout()
plt.show()