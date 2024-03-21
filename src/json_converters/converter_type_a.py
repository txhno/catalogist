import pandas as pd
import json
import os

file_path = 'csvs/cleaned/sku_list_1_cleaned.csv'
df = pd.read_csv(file_path)

def parse_sku_data(df):
    products = []
    current_category = ""
    for index, row in df.iterrows():
        # Identify category rows and update the current category
        if pd.isnull(row['PROBLEMSOLUTION']) and not pd.isnull(row['Unnamed: 1']) and pd.isnull(row['Unnamed: 2']):
            current_category = row['Unnamed: 1']
        # Identify SKU rows by checking if the first cell contains an ID (numeric)
        elif not pd.isnull(row['PROBLEMSOLUTION']) and row['PROBLEMSOLUTION'].isdigit():
            sku = {
                "ID": int(row['PROBLEMSOLUTION']),
                "title": current_category,
                "description": row['Unnamed: 1'],
                "price": int(row['Unnamed: 3'].replace(',', '')),
                "attributes": {}
            }
            # Extract additional attributes if available
            if not pd.isnull(row['Unnamed: 2']):
                sku["attributes"]["Pack Size"] = row['Unnamed: 2']
            products.append(sku)
    return products

# Parse the SKU data starting from the header row for SKU details
structured_sku_data = parse_sku_data(df[25:])
output_dir = 'exported-jsons'
output_file = 'sku_list_1.json'
os.makedirs(output_dir, exist_ok=True)
full_path = os.path.join(output_dir, output_file)

with open(full_path, 'w', encoding='utf-8') as f:
    json.dump(structured_sku_data, f, indent=4)

print(f"Saved \"sku_list_1.json\"")