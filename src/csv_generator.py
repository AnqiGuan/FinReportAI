import os
import pandas as pd
import re

txt_path = "outputs/extracted_text.txt"
csv_path = "outputs/financial_data.csv"


with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

dates = ["12/31/2024", "12/31/2023", "12/31/2022", "12/31/2021"]

fields = {
    "Total Assets": [],
    "Total Liabilities": [],
    "Total Equity": [],
    "Total Capitalization": [],
    "Common Stock Equity": [],
    "Capital Lease Obligations": [],
    "Net Tangible Assets": [],
    "Working Capital": [],
    "Invested Capital": [],
    "Tangible Book Value": [],
    "Total Debt": [],
    "Net Debt": [],
    "Share Issued": [],
    "Ordinary Shares Number": [],
    "Treasury Shares Number": []
}


for field in fields.keys():
    field_found = False  
    extracted_values = []

    for i, line in enumerate(lines):
        if field in line:
            field_found = True
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            numbers = re.findall(r"-?\d{1,3}(?:,\d{3})*", line) 
            numbers = [int(n.replace(",", "")) for n in numbers if re.match(r"-?\d+", n.replace(",", ""))]
            extracted_values = numbers[:len(dates)] 

    while len(extracted_values) < len(dates):
        extracted_values.append(None) 

    fields[field] = extracted_values


data = {"Date": dates}
data.update(fields)

df_corrected = pd.DataFrame(data)

df_corrected.to_csv(csv_path, index=False, encoding="utf-8")