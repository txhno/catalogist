import pandas as pd
import json
import os

# Function to check if a value can be converted to an integer
def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

file_path = 'csvs/cleaned/sku_list_4_cleaned.csv'
df_cleaned = pd.read_csv(file_path, header=None, dtype=str)

# Clean the DataFrame from NaN columns and rows that are completely NaN
df_cleaned = df_cleaned.dropna(axis=1, how='all').dropna(how='all')

# Ensure all data is treated as strings during parsing to prevent errors
data_list = df_cleaned.astype(str).values.tolist()

def parse_four_column_table_corrected(data):
    skus = []
    current_title = ""
    for row in data:
        # Use is_int() to check if the first column is an integer (SL.NO.)
        if is_int(row[0]):
            try:
                sl_no = int(row[0])
                product_category = row[1].strip()
                model_name = row[2].strip()
                bare_tool_part_no = row[3].strip()

                if product_category != "":
                    current_title = product_category

                sku = {
                    "ID": sl_no,
                    "title": current_title,
                    "description": model_name,
                    "price": None,  # Placeholder for price, as it's not provided in this snippet
                    "attributes": {
                        "Bare Tool Part No": bare_tool_part_no
                    }
                }
                skus.append(sku)
            except (ValueError, IndexError):
                # Handle unexpected row format or missing data
                continue
        else:
            # Skip rows not starting with an integer SL.NO., including title or malformed rows
            continue
    return skus

skus_extracted = parse_four_column_table_corrected(data_list)

output_dir = 'exported-jsons'
os.makedirs(output_dir, exist_ok=True)

output_file_path = os.path.join(output_dir, 'sku_list_4.json')
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(skus_extracted, f, indent=4)

print(f"Saved \"sku_list_4.json\"")