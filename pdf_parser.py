import fitz
import re
import json

def extract_skus(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from each page
    for page in doc:
        text += page.get_text()
    
    doc.close()

    # Regular expression to identify each product's start and parse its details
    sku_pattern = re.compile(
        r'(\d+)\s+(LOCTITE.*?)(\d+\s*ml|g|oz|kg|lb|IN x \d+ FT|Kit)\s+(\d+,\d+|\d+)\s', re.DOTALL
    )
    
    matches = sku_pattern.findall(text.replace('\n', ' '))

    # Extract and structure the SKU Details to JSON
    skus = []
    for id, title_description, pack_size, price in matches:
        # Separate title and description if applicable
        title_parts = title_description.split(' ', 2)
        if len(title_parts) > 2:
            title = title_parts[0] + ' ' + title_parts[1]
            description = title_parts[2]
        else:
            title = title_description
            description = ""

        skus.append({
            "ID": int(id),
            "title": title.strip(),
            "description": description.strip(),
            "price": int(price.replace(',', '')), 
            "attributes": {"Pack Size": pack_size.strip()}
        })

    return skus

# Path to the PDF file
pdf_path = 'SKU_Pricelist_1.pdf'
extracted_skus = extract_skus(pdf_path)

# Export to a JSON file
json_path = 'extracted_skus.json'
with open(json_path, 'w') as f:
    json.dump(extracted_skus, f, indent=4)

print(f"Extracted {len(extracted_skus)} SKUs to {json_path}")
