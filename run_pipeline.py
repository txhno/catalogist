import subprocess
import os

def run_script(script_path):
    """Executes a given Python script using subprocess."""
    try:
        subprocess.check_call(['python3', script_path])
        print(f"Successfully executed {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {script_path}: {e}")

def main():
    run_script('src/pdf_extractor.py')  # Step 1: Extract PDFs to CSVs
    run_script('src/csv_cleaner.py')    # Step 2: Clean extracted CSVs
    converter_scripts = [               # Step 3: Convert cleaned CSVs to JSONs using converter scripts
        'converter_type_a.py',
        'converter_type_b.py',
        'converter_type_c.py',
        'converter_type_d.py',
        'converter_type_e.py',
        'converter_type_f.py'
    ]
    
    for script_name in converter_scripts:
        script_path = os.path.join('src/json_converters', script_name)
        run_script(script_path)

    print("All PDFs have been successfully exported to JSONs at /exported-jsons/.")

if __name__ == "__main__":
    main()
