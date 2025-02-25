"""This code takes The_Weekly.csv as it's input. It takes the first page of each pdf in the csv
and combines it into a single text file."""

import pandas as pd
import requests
import fitz  # PyMuPDF
from pathlib import Path
from io import BytesIO

# Load the DataFrame from the previous script
csv_path = Path("/Users/sarahpawlowski/Documents/spaceWeather_RiskCommStudy/01_Data/TextBasedData/Email_Alerts/NOAA_Alerts/The_Weekly.csv")
df = pd.read_csv(csv_path)

# Output file to store all the combined text
output_filename = "Txt_The_Weekly.txt"

with open(output_filename, "w", encoding="utf-8") as outfile:
    for index, row in df.iterrows():
        pdf_url = row["File Link"]  # Adjust column name if different

        # Download the PDF file
        response = requests.get(pdf_url)
        if response.status_code == 200:
            pdf_data = BytesIO(response.content)  # Read PDF into memory
            doc = fitz.open(stream=pdf_data, filetype="pdf")

            if len(doc) > 0:  # Ensure the PDF has at least one page
                first_page_text = doc[0].get_text("text")

                # Write to output file with a separator
                outfile.write(f"=== File from {row['Year']} ===\n")
                outfile.write(first_page_text)
                outfile.write("\n\n")

                print(f"Successfully added: {pdf_url}")
            doc.close()

print(f"All extracted text saved in {output_filename}")