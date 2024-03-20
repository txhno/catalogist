import pandas as pd
import json
import re

# Define helper functions for parsing
def parse_dimensions(dimensions_str):
    """Extract dimensions from the string."""
    match = re.search(r'(\d+)\s*x\s*(\d+)\s*x\s*(\d+)', dimensions_str)
    if match:
        return {"Length": match.group(1), "Width": match.group(2), "Height": match.group(3)}
    return {}

def parse_catalog_no_and_price(details_str):
    """Extract catalog number and price."""
    details = details_str.split(' ')
    price = None
    try:
        price = float(details[-1].replace(',', '').replace('̀/-', ''))
    except ValueError:
        pass
    catalog_no = ' '.join(details[:-1])
    return catalog_no, price

def is_sku_line(line):
    """Determine if a line contains SKU data."""
    return bool(re.search(r'\d+\s*x\s*\d+\s*x\s*\d+', line)) or "sq.mm" in line

def parse_sku_line(line, title):
    """Parse a single SKU line into structured data."""
    parts = [part.strip() for part in line.split(',') if part.strip()]
    sku = {
        "ID": None,
        "title": title,
        "description": "",
        "price": None,
        "attributes": {}
    }

    for part in parts:
        if "sq.mm" in part:
            sku["attributes"]["Cable Size"] = part
        elif re.search(r'\d+\s*x\s*\d+\s*x\s*\d+', part):
            sku["attributes"]["Dimensions"] = parse_dimensions(part)
        elif part.strip().isdigit():
            sku["attributes"]["Packing Quantity"] = part.strip()
        else:
            catalog_no, price = parse_catalog_no_and_price(part)
            sku["ID"] = catalog_no
            sku["price"] = price

    return sku

file_path = 'csvs/cleaned/sku_list_3_cleaned.csv'
df = pd.read_csv(file_path, dtype=str, header=None)

skus = []
current_title = ""
for index, row in df.iterrows():
    line = ','.join(row.dropna().astype(str))
    if is_sku_line(line):
        sku = parse_sku_line(line, current_title)
        skus.append(sku)
    else:
        current_title = line

output_dir = 'exported-jsons/sku_list_3.json'
with open(output_dir, 'w', encoding='utf-8') as json_file:
    json.dump(skus, json_file, indent=4)

print(f"Saved \"sku_list_3.json\"")