import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import matplotlib.dates as mdates

def fetch_noaa_data(url):
    response = requests.get(url)
    data = response.json()
    return data[1:]  # Skip the header row

def extract_values(data):
    timestamps = [datetime.datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S.%f") for entry in data]
    k_index_values = [float(entry[1]) for entry in data]
    return timestamps, k_index_values

def plot_k_index(timestamps, k_index_values):
    colors = []
    for value in k_index_values:
        if 5 <= value < 6:
            colors.append('yellow')
        elif 6 <= value < 7:
            colors.append('gold')
        elif 7 <= value < 8:
            colors.append('orange')
        elif 8 <= value < 9:
            colors.append('red')
        elif value >= 9:
            colors.append('darkred')
        else:
            colors.append('lightgreen')

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.subplots_adjust(left=0.15, right=0.75)
    ax.bar(timestamps, k_index_values, color = colors, width = 0.1)
    ax.set_xlabel('Time')
    ax.set_ylabel('NOAA Kp Index')
    ax.set_title('Estimated Planetary K index (3 hour data)')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Show every 3rd hour
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Show only hour:minute
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis = 'y', alpha = 0.5)

    legend_patches = [
        mpatches.Patch(color='lightgreen', label='Kp < 5'),
        mpatches.Patch(color='yellow', label='5 ≤ Kp < 6'),
        mpatches.Patch(color='gold', label='6 ≤ Kp < 7'),
        mpatches.Patch(color='orange', label= '7 ≤ Kp < 8'),
        mpatches.Patch(color='red', label='8 ≤ Kp < 9'),
        mpatches.Patch(color='darkred', label=' Kp < 9')
    ]
    ax.legend(handles=legend_patches, title="K-Index Levels", loc='center left',
              bbox_to_anchor=(1.02, 0.5), frameon=False, handletextpad=1.5)
    plt.tight_layout
    plt.show()

if __name__ == "__main__":
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    data = fetch_noaa_data(url)
    timestamps, k_index_values = extract_values(data)
    plot_k_index(timestamps, k_index_values)