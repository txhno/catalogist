# SKU List Parser

Transform SKU Price Lists from PDF to JSON: Automated extraction, cleaning, and conversion pipeline for SKU data.

## Overview

This repository contains a Python-based solution for converting SKU (Stock Keeping Unit) price lists from PDF format into structured JSON objects. It handles both PDFs with and without boundary lines around tables, applies data cleaning to remove unwanted information, and exports the cleaned data into JSON files where each object represents an SKU with its attributes.

## Prerequisites

- Python 3.8 or higher
- Java 8 or higher (required by tabula-py)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/txhno/sku-list-parser.git
   cd sku-list-parser
   ```

2. Install required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Ensure Java (version 8 or above) is installed and properly set up on your system. You can verify this by running:
   ```sh
   java -version
   ```
   If Java is not installed, please install it from [Oracle Java](https://www.oracle.com/java/technologies/javase-jdk8-downloads.html) or your preferred source.

## Usage

1. SKU pricelist PDFs are present in the `pdfs/boundaried` or `pdfs/unboundaried` directories, depending on whether PDFs have boundary lines around their tables.

2. Run the pipeline script:
   ```sh
   python3 run_pipeline.py
   ```

This script will process all PDFs, extract and clean CSV data, and then convert them into JSON files. The JSON files will be saved in the `exported-jsons` directory.

### Dynamic PDF Parser

For dynamic PDF to JSON parsing and conversion, open and run the `dynamic_pdf_to_json.ipynb` Jupyter notebook after installing requirements. 

This notebook provides a step-by-step guide for converting specific PDF pages to structured JSON data using the Gemini Pro Vision model. It specializes in converting SKU pricelist PDFs, including those based on images, into structured JSONs. The model settings can be configured within the notebook, allowing for precise data extraction tailored to your needs. Additionally, the range of PDF pages to be converted can also be specified and adjusted as required.
Ensure all prerequisites are installed, and follow the notebook's instructions for tailored SKU data processing.

## Project Structure

- `pdfs/boundaried` and `pdfs/unboundaried`: Directories to place your PDF files for processing.
- `src`: Contains the Python scripts for the pipeline steps.
  - `pdf_extractor.py`: Extracts tables from PDFs to CSV format.
  - `csv_cleaner.py`: Cleans the extracted CSV files.
  - `json_converters`: Contains various converter scripts to transform cleaned CSVs into JSON format.
- `exported-jsons`: The output directory where the JSON files are saved.

## Built With

- [Python](https://www.python.org/) - The primary programming language used.
- [pandas](https://pandas.pydata.org/) - Data manipulation and analysis library.
- [tabula-py](https://github.com/chezou/tabula-py) - Python wrapper for Tabula, used to extract tables from PDFs into pandas DataFrames.
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/tools/knowledge-retrieval) - Leveraged the knowledge-retrieval tool to create unique JSON converters for the CSVs.


## Contributing

Contributions to the SKU List Parser project are welcome! Please submit pull requests or open issues to suggest improvements or report bugs.

## Authors

- **Roshan Warrier** - *Project Owner* - [Txhno](https://github.com/txhno)
