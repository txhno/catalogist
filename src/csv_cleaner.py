import csv
import os
import glob

input_dir = 'csvs/extracted'
output_dir = 'csvs/cleaned'
os.makedirs(output_dir, exist_ok=True)

csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

def contains_forbidden_word(cell):
    forbidden_words = ["mumbai", "tejeet"]
    return any(word.lower() in cell.lower() for word in forbidden_words)  # Case insensitive match

def fix_csv(input_file_path, output_file_path):
    with open(input_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Determine the maximum number of columns in any row
    max_cols = max(len(row) for row in rows)

    adjusted_rows = []
    for row in rows:
        # Check for and skip rows based on specified conditions
        non_empty_cells = [cell for cell in row if cell.strip() not in ['', '()']]
        if len(non_empty_cells) == 0 or any(contains_forbidden_word(cell) for cell in row) \
           or any("Price List" in cell for cell in row) \
           or all(cell.strip() == '' for cell in row) \
           or any(len(cell) >= 120 for cell in row) \
           or (len(non_empty_cells) == 1 and non_empty_cells[0].isdigit()):
            continue  # Skip row based on the conditions above

        # Ensure rows have a uniform number of columns
        adjusted_row = row + [''] * (max_cols - len(row))
        adjusted_rows.append(adjusted_row)

    # Write the adjusted rows to the new CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(adjusted_rows)

for csv_file in csv_files:
    base_name = os.path.basename(csv_file)
    output_file_name = os.path.splitext(base_name)[0].replace('_extracted', '') + "_cleaned.csv"
    output_file_path = os.path.join(output_dir, output_file_name)
    
    fix_csv(csv_file, output_file_path)

print("All CSVs have been cleaned.")