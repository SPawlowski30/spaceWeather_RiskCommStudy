import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data from the JSON file
url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
response = requests.get(url)
data = response.json()

# Filter and get data for graph
filtered_data = [entry for entry in data if entry.get("energy") == "0.1-0.8nm"]
times = [datetime.strptime(entry.get("time_tag"), "%Y-%m-%dT%H:%M:%SZ") for entry in filtered_data]
fluxes = [entry.get("flux") for entry in filtered_data]

# Plot flux vs time
plt.figure(figsize=(10, 6))
plt.plot(times, fluxes)
plt.xlabel('Time')
plt.ylabel('Watts * m^-2')
plt.title('GOES X-Ray Flux (1-minute data)')
plt.yscale('log')
plt.ylim(10**-9, 10**-2)
plt.grid(axis='y', alpha=0.5)
plt.xlim(min(times))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()