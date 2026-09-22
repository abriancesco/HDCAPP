import csv
import re
from datetime import datetime

INPUT = "landata1.csv"
OUTPUT = "landata1_fixed.csv"

# Extract first numeric value (deeded acreage)
def extract_first_number(text):
    if not text:
        return ""
    match = re.search(r"[\d,.]+", text)
    if not match:
        return ""
    num = match.group(0)
    num = num.replace(",", "")
    return num

# Normalize dates into YYYY-MM-DD
def fix_date(val):
    if not val:
        return ""
    val = val.strip()

    # Try common Access formats
    formats = [
        "%m/%d/%Y", "%m/%d/%y",
        "%m-%d-%Y", "%m-%d-%y",
        "%Y-%m-%d",  # already correct
    ]

    for fmt in formats:
        try:
            d = datetime.strptime(val, fmt)
            return d.strftime("%Y-%m-%d")
        except:
            pass

    # If nothing matches, return empty
    return ""

# Acreage fields to clean
ACRE_FIELDS = [
    "SIZE",
    "SizeTotalAcres",
    "Deeded Size",
    "NMSL Size",
    "SLO Size",
    "BLM Size",
]

# Date fields to clean
DATE_FIELDS = [
    "SALEDATE",
    "LISTING_DATE",
    "PREVIOUS_SALE_DATE",
    "VERI_DATE",
    "INSP_DATE",
]

with open(INPUT, newline="", encoding="utf-8-sig") as infile, \
     open(OUTPUT, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:

        # Clean acreage fields
        for col in ACRE_FIELDS:
            if col in row:
                row[col] = extract_first_number(row[col])

        # Clean date fields
        for col in DATE_FIELDS:
            if col in row:
                row[col] = fix_date(row[col])

        writer.writerow(row)

print("CSV cleaned. Output written to:", OUTPUT)
