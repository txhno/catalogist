import tabula
import glob
import os

print("Initializing PDF extraction.")

directories = {
    "pdfs/boundaried": True,  # Use lattice mode for PDFs in 'boundaried' directory [PDFs which have tables with marking lines]
    "pdfs/unboundaried": False,  # Do not use lattice mode for PDFs in 'unboundaried' directory [PDFs which have tables without marking lines]
}

output_dir = "csvs/extracted"
os.makedirs(output_dir, exist_ok=True)

for directory, use_lattice in directories.items():
    # Find all PDF files in the current directory
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    
    for pdf_path in pdf_files:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_csv_path = os.path.join(output_dir, f"{base_name}_extracted.csv")
        
        print(f"Extracting from {pdf_path}.")
        tabula.convert_into(pdf_path, output_csv_path, output_format="csv", pages='all', lattice=use_lattice)
        print(f"Extracted and saved to {output_csv_path}.")

print("All PDFs have been successfully extracted to CSVs.")
