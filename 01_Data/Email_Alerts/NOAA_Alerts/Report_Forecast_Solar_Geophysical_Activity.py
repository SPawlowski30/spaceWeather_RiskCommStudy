import requests
from bs4 import BeautifulSoup
import random
import urllib.parse
import pandas as pd

# Base URL for the parent directory
base_url = "https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/reports_solar_geophysical_activity/"

# list of years 2020 - 2025
years = list(range(2020, 2026))  # 2020 to 2025


# Function to get all subdirectory links (months)
def get_subdirectories(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [urllib.parse.urljoin(url, a["href"]) for a in soup.find_all("a", href=True) if a["href"].endswith("/")]


# Function to get all text files from a given month
def get_text_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [urllib.parse.urljoin(url, a["href"]) for a in soup.find_all("a", href=True) if a["href"].endswith(".txt")]


# Collect all text file links per year
yearly_files = {year: [] for year in years}

for year in years:
    year_url = urllib.parse.urljoin(base_url, f"{year}/")  # Construct the year URL
    month_links = get_subdirectories(year_url)  # Get monthly subdirectories

    for month in month_links:
        yearly_files[year].extend(get_text_files(month))  # Collect text file links

# Calculate the number of files to select per year
total_files = sum(len(files) for files in yearly_files.values())
num_to_select = max(1, int(0.1 * total_files))  # Select 10% overall

files_per_year = num_to_select // len(years)  # Equal distribution
selected_files = []

for year, files in yearly_files.items():
    if len(files) >= files_per_year:
        selected_files.extend([(year, file) for file in random.sample(files, files_per_year)])  # Random selection
    else:
        selected_files.extend([(year, file) for file in files])  # If fewer files exist, take all available

# Now create the DataFrame correctly
df = pd.DataFrame(selected_files, columns=["Year", "File Link"])
print(f"Total rows in df: {df.shape[0]}")
print(df.head())