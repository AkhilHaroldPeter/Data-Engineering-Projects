from File_content_generator import *
from create_doc import *
from create_pdf import *
from configparser import RawConfigParser
import sys
import pandas as pd
from convert_to_tuple_format import *
from pathlib import Path
import os
from datetime import datetime
from read_sql_file import *
from setup_logging import *

# Set up logging for monitoring
setup_logging()

try:
    logging.info(f"#"*50)
    logging.info(f"STEP 4 : GENERATING OUTPUTS")
    logging.info(f"#"*50)    
    # Get the filename from command-line arguments
    filename = sys.argv[1]
    logging.info(f"Processing file: {filename}")

    current_directory = Path(os.getcwd()).resolve().parent
    config_path = current_directory / 'config' / 'iconfig.ini'
    output_path = current_directory / 'data' / 'output'
    sql_files_path = current_directory / 'sql'

    # Get the current date and time
    current_date = datetime.now().date()
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Format for folder name

    # Create date and datetime folders within the output path
    date_folder = output_path / str(current_date)
    datetime_folder = date_folder / current_datetime

    # Create the folders if they do not exist
    datetime_folder.mkdir(parents=True, exist_ok=True)

    # If you want to create a specific folder for the filename:
    filename_folder = datetime_folder / filename
    filename_folder.mkdir(parents=True, exist_ok=True)
    logging.info(f"Created folder structure for: {filename_folder}")

    # Load configuration
    config = RawConfigParser()
    config.read(config_path)
    logging.info(f"Loaded configuration from: {config_path}")

    # Read output preferences from config
    Excel_output = config.getboolean(f'{filename}', 'Excel_output')
    csv_output = config.getboolean(f'{filename}', 'csv_output')
    json_output = config.getboolean(f'{filename}', 'json_output')
    parquet_output = config.getboolean(f'{filename}', 'parquet_output')
    pdf_output = config.getboolean(f'{filename}', 'pdf_output')
    word_output = config.getboolean(f'{filename}', 'word_output')
    generate_content = config.getboolean(f'{filename}', 'generate_content')
    query_file_name = config[f'{filename}']['query_file_name']

    # Read the input DataFrame from stdin
    df = pd.read_csv(sys.stdin)
    logging.info(f"Read DataFrame with {len(df)} rows")

    if generate_content:
        logging.info("Generating content using File_content_generator...")
        description_list = File_content_generator(df)  # Add additional parameters as needed

    # Check each output format and write directly if True
    if Excel_output:
        excel_path = filename_folder / f'{filename}_report.xlsx'
        df.to_excel(excel_path, index=False)
        logging.info(f"Excel report saved to: {excel_path}")

    if csv_output:
        csv_path = filename_folder / f'{filename}_report.csv'
        df.to_csv(csv_path, index=False)
        logging.info(f"CSV report saved to: {csv_path}")

    if json_output:
        json_path = filename_folder / f'{filename}_report.json'
        df.to_json(json_path, orient='records', lines=True)
        logging.info(f"JSON report saved to: {json_path}")

    if parquet_output:
        parquet_path = filename_folder / f'{filename}_report.parquet'
        df.to_parquet(parquet_path, index=False)
        logging.info(f"Parquet report saved to: {parquet_path}")

    if pdf_output:
        pdf_output_path = filename_folder / f"{filename}_Report.pdf"
        create_pdf(str(pdf_output_path), f"{filename.replace('_', ' ')}", description_list, df)
        logging.info(f"PDF report saved to: {pdf_output_path}")

    if word_output:
        doc_output_path = filename_folder / f'{filename}_Report.docx'
        create_doc(
            doc_output_path,
            f"{filename.replace('_', ' ')}",
            config[f'{filename}']['word_output_text_intro'],
            description_list,
            convert_to_tuple_format(df),
            df.columns
        )
        logging.info(f"Word document saved to: {doc_output_path}")

except Exception as e:
    logging.error(f"An error occurred: {e}", exc_info=True)

