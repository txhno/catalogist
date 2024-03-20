import pandas as pd
import json

# Function to clean and standardize header names
def clean_header(header):
    return header.replace('\r', ' ').replace('`', '').strip()

# Function to parse and transform data to the required JSON format
def parse_data_to_json_updated(data):
    products = []
    is_table = False
    headers = []
    table_start_index = None

    for index, row in data.iterrows():
        row_values = row.dropna().values

        if "Type" in row_values or "Cat. No." in row_values:
            is_table = True
            table_start_index = index
            headers = [clean_header(str(val)) for val in row_values if str(val).strip()]
            continue

        if is_table and index > table_start_index:
            if len(row_values) == 0 or "Type" in row_values or "Cat. No." in row_values:
                is_table = False
                table_start_index = None
                headers = []
                continue
            
            product_info = {}
            for i, value in enumerate(row_values):
                if i >= len(headers):
                    break
                key = headers[i]
                value = value.replace('\r', ' ').replace('`', '').strip()

                if key in ["Cat. No.", "ID"]:
                    product_info["ID"] = value
                elif key == "Type":
                    product_info["description"] = value
                elif key in ["M.R.P. Per Unit", "M.R.P. () Per Unit"]:
                    try:
                        product_info["price"] = float(value.replace('*', '').strip().replace(',', ''))
                    except ValueError:
                        product_info["price"] = value
                else:
                    if "attributes" not in product_info:
                        product_info["attributes"] = {}
                    product_info["attributes"][key] = value

            if "ID" in product_info:
                products.append(product_info)

    return products

def main():
    file_path = 'csvs/cleaned/sku_list_5_cleaned.csv'  # Updated path
    data = pd.read_csv(file_path, header=None)
    products_json_updated = parse_data_to_json_updated(data)

    output_file_path_updated = 'exported-jsons/sku_list_5.json'  # Updated output path
    with open(output_file_path_updated, 'w', encoding='utf-8') as f:
        json.dump(products_json_updated, f, indent=4)

    print(f"Saved \"sku_list_5.json\"")

if __name__ == "__main__":
    main()
