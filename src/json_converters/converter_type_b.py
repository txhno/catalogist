import pandas as pd
import json

# Function to safely convert price strings to float values
def safe_convert_price(price_str):
    try:
        return float(price_str.replace(",", "").strip())
    except ValueError:
        return 0.0

# Correcting the input and output file paths relative to the script location
file_path = 'csvs/cleaned/sku_list_2_cleaned.csv'
corrected_output_file_path = 'exported-jsons/sku_list_2.json'

# Re-reading the CSV to start fresh
data = pd.read_csv(file_path, dtype=str, header=None)

# Identifying table sections
def find_table_sections(df):
    sections = []
    current_section = None
    for index, row in df.iterrows():
        if pd.notna(row[0]) and pd.isna(row[1]) and pd.isna(row[2]):
            if current_section:
                current_section['end_index'] = index - 1
                sections.append(current_section)
            current_section = {'start_index': index + 2}
        elif index == len(df) - 1:
            current_section['end_index'] = index
            sections.append(current_section)
    return sections

sections = find_table_sections(data)

# Parsing identified sections
skus = []
for section in sections:
    table_df = data.iloc[section['start_index']:section['end_index'] + 1, :].dropna(how='all', axis=1).reset_index(drop=True)
    table_title = data.iloc[section['start_index'] - 3, 0]
    
    for _, row in table_df.iterrows():
        if pd.isna(row[0]) or 'Part No' in row[0]:
            continue
        sku = {
            "ID": row[0].strip(),
            "title": table_title.strip(),
            "description": row[1].strip() if len(row) > 1 and pd.notnull(row[1]) else "",
            "price": safe_convert_price(row[3]) if len(row) > 3 and pd.notnull(row[3]) else 0.0,
            "attributes": {}
        }
        if len(row) > 5 and pd.notnull(row[5]):
            sku["attributes"]["Spares MRP Per Number in CL"] = safe_convert_price(row[5])
        if len(row) > 6 and pd.notnull(row[6]):
            sku["attributes"]["Spares MRP Per Number in SZL"] = safe_convert_price(row[6])
        skus.append(sku)

# Formatting the adjusted SKU details into JSON
corrected_json_skus = json.dumps(skus, indent=4, ensure_ascii=False)

with open(corrected_output_file_path, 'w', encoding='utf-8') as f:
    f.write(corrected_json_skus)

print(f"Saved \"sku_list_2.json\"")