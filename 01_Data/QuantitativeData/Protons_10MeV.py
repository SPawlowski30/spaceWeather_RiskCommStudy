import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from JSON
url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json"
response = requests.get(url)
data = response.json()

# Filter and get data for graph
filtered_data = [entry for entry in data if entry.get("energy") == ">=10 MeV"]
times = [datetime.strptime(entry.get("time_tag"), "%Y-%m-%dT%H:%M:%SZ") for entry in filtered_data]
fluxes = [entry.get("flux") for entry in filtered_data]

# Plots flux vs time
plt.figure(figsize=(10, 6))
plt.plot(times, fluxes)
plt.xlabel('Time')
plt.ylabel('pfu (proton fluence unit)')
plt.title('GOES Proton Flux (5-minute data)')
plt.yscale('log')
plt.ylim(10**-2, 10**4)
plt.xlim(min(times))
plt.axhline(y=10**1, color='red', linestyle='--', label='SWPC 10MeV Warning Threshold')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()