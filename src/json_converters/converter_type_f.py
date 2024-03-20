import pandas as pd
import json

def is_valid_sku_row(row):
    """Check if the row could potentially contain SKU data."""
    return any(isinstance(item, str) and item.strip() for item in row)

def parse_3_or_4_col_table(row):
    """Parse rows from 3 or 4 column SKU tables."""
    try:
        cat_nos, description, _, pack = row[:4]
        sku_id = cat_nos.replace(" ", "")
        return {"ID": sku_id, "description": description, "attributes": {"Pack": pack}}
    except ValueError:
        return None

def parse_longer_table(row):
    """Parse rows from the longer SKU table format, handling irregular data."""
    try:
        title_desc = str(row[0]) if pd.notna(row[0]) else ""
        rated_current = str(row[1]) if pd.notna(row[1]) else ""
        p3_cat_nos = str(row[2]).replace(" ", "") if pd.notna(row[2]) else ""
        p4_cat_nos = str(row[4]).replace(" ", "") if pd.notna(row[4]) else ""

        if "," in title_desc:
            title, description = title_desc.split(",", 1)[0].strip(), title_desc.split(",", 1)[1].strip()
        else:
            title, description = title_desc, ""
        
        skus = []
        if p3_cat_nos:
            skus.append({"ID": p3_cat_nos, "title": title, "description": description, "attributes": {"Rated Current": rated_current, "Type": "3P"}})
        if p4_cat_nos:
            skus.append({"ID": p4_cat_nos, "title": title, "description": description, "attributes": {"Rated Current": rated_current, "Type": "4P"}})

        return skus
    except ValueError:
        return None


csv_file_path = 'csvs/cleaned/sku_list_6_cleaned.csv'

# Read the CSV file, assuming variable number of fields per row
df_flexible = pd.read_csv(csv_file_path, header=None, engine='python', on_bad_lines='skip')

# Process the CSV file to extract SKU details
skus = []
for row in df_flexible.itertuples(index=False):
    if not is_valid_sku_row(row):
        continue
    
    parsed_sku = None
    if len(row) >= 5:
        parsed_sku = parse_longer_table(row)
    elif 2 <= len(row) <= 4:
        parsed_sku = parse_3_or_4_col_table(row)
    
    if parsed_sku:
        if isinstance(parsed_sku, list):
            skus.extend(parsed_sku)
        else:
            skus.append(parsed_sku)

# Removing empty or incomplete SKUs
skus = [sku for sku in skus if sku and "ID" in sku]

output_json_path = 'exported-jsons/sku_list_6.json'
with open(output_json_path, 'w') as f:
    json.dump(skus, f, indent=4)

print(f"Saved \"sku_list_6.json\"")
