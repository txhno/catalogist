import tabula
import glob
import os
import concurrent.futures

print("Initializing PDF extraction.")

directories = {
    "pdfs/boundaried": True,  # Use lattice mode for PDFs in 'boundaried' directory [PDFs which have tables with marking lines]
    "pdfs/unboundaried": False,  # Do not use lattice mode for PDFs in 'unboundaried' directory [PDFs which have tables without marking lines]
}

output_dir = "csvs/extracted"
os.makedirs(output_dir, exist_ok=True)

def process_pdf(pdf_path, use_lattice):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_csv_path = os.path.join(output_dir, f"{base_name}_extracted.csv")
    
    print(f"Extracting from {pdf_path}.")
    tabula.convert_into(pdf_path, output_csv_path, output_format="csv", pages='all', lattice=use_lattice)
    print(f"Extracted and saved to {output_csv_path}.")

# Using ProcessPoolExecutor to parallelize PDF extraction
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Submit tasks for each PDF
    futures = []
    for directory, use_lattice in directories.items():
        pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
        for pdf_path in pdf_files:
            futures.append(executor.submit(process_pdf, pdf_path, use_lattice))
    
    # Wait for all futures to complete
    concurrent.futures.wait(futures)

print("All PDFs have been successfully extracted to CSVs.")
