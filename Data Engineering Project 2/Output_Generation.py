from File_content_generator import *
from create_doc import *
from create_pdf import *
from configparser import RawConfigParser
import sys
import pandas as pd
from convert_to_tuple_format import *


# Load configuration
config = RawConfigParser()
config.read('iconfig.ini')

# Get the filename from command-line arguments
filename = sys.argv[1]

# Read output preferences from config
Excel_output = config.getboolean(f'{filename}', 'Excel_output')
csv_output = config.getboolean(f'{filename}', 'csv_output')
json_output = config.getboolean(f'{filename}', 'json_output')
parquet_output = config.getboolean(f'{filename}', 'parquet_output')
pdf_output = config.getboolean(f'{filename}', 'pdf_output')
word_output = config.getboolean(f'{filename}', 'word_output')
generate_content = config.getboolean(f'{filename}', 'generate_content')


# Read the input DataFrame from stdin
df = pd.read_csv(sys.stdin)
if generate_content:
    description_list = File_content_generator(df)


# Check each output format and write directly if True
if Excel_output:
#     excel_path = config[f'{filename}']['Excel_output_path']
    df.to_excel(f'{filename}_report.xlsx', index=False)  # Write to Excel

if csv_output:
#     csv_path = config[f'{filename}']['csv_output_path']
    df.to_csv(f'{filename}_report.csv', index=False)  # Write to CSV

if json_output:
#     json_path = config[f'{filename}']['json_output_path']
    df.to_json(f'{filename}_report.json', orient='records', lines=True)  # Write to JSON

if parquet_output:
#     parquet_path = config[f'{filename}']['parquet_output_path']
    df.to_parquet(f'{filename}_report.parquet', index=False)  # Write to Parquet


if pdf_output:
    create_pdf(f"{filename}_.pdf", f"{filename.replace('_',' ')}", description_list, df)

# Here the parameter 4 passed in create_doc is genereated by an llm model(cohere)    
if word_output:
    create_doc(f'{filename}_Report.docx', f"{filename.replace('_',' ')}", 
    config[f'{filename}']['word_output_text_intro'], 
    description_list, 
    convert_to_tuple_format(df),
    df.columns)

