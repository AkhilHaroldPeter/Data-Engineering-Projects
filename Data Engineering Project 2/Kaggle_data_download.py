import pandas as pd
import sys
import requests
import io
import logging
import zipfile
from configparser import RawConfigParser
from setup_logging import *

config = RawConfigParser()
config.read('iconfig.ini')

# Set up logging for monitoring
# logging.basicConfig(level=logging.INFO)
# setup_logging()
setup_logging(is_session_log=True) 

# Kaggle dataset URL and API key
dataset_url = config['Kaggle_data_download']['dataset_url']
headers = {'Authorization': 'Bearer <your-kaggle-api-key>'}

# Chunk size for processing large datasets (adjust based on memory constraints)
chunk_size = 10000  # Adjust this as necessary
final_df = pd.DataFrame()


try:
    logging.info(f"#"*50)
    logging.info(f"STEP 1 : Extarcting data from kagggle")
    logging.info(f"#"*50)    
    # Start downloading dataset
    logging.info("Starting data download...")
    response = requests.get(dataset_url, headers=headers, stream=True)
    response.raise_for_status()  # Raise an error for bad responses

    # Unzip the downloaded file in memory and process the contents
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        # List the files in the zip archive
        file_list = zip_ref.namelist()
        logging.info(f"Files in the zip archive: {file_list}")

        # Extract the CSV file
        with zip_ref.open(file_list[0]) as file:
            # Read data in chunks for memory-efficient processing
            logging.info("Processing the data in chunks...")
            for chunk in pd.read_csv(file, chunksize=chunk_size):
               
                cleaned_chunk = chunk
                chunk.rename(columns={'index':'transaction_id','City':'city','Date':'transaction_date',
                                     'Card Type':'card_type','Exp Type':'exp_type','Gender':'gender','Amount':'amount'},inplace=True)
                chunk['transaction_id']+=1
                cleaned_chunk = chunk
                final_df = pd.concat([final_df,cleaned_chunk])
                # Print cleaned data (for testing)
                logging.info(f"Processed {len(cleaned_chunk)} rows of data.")
                
                # Write the cleaned data to stdout for NiFi to pick up
#                 cleaned_chunk.to_csv(sys.stdout, index=False, header=False)  # Exclude header after the first chunk
#             final_df.to_csv('output.csv', index=False, header=True)
            final_df.to_csv(sys.stdout, index=False, header=True)
    logging.info("Data processing and transmission to NiFi completed successfully.")

except requests.exceptions.RequestException as e:
    logging.error(f"Failed to download dataset: {e}")
except pd.errors.EmptyDataError:
    logging.error("No data found in the response.")
except zipfile.BadZipFile:
    logging.error("The downloaded file is not a valid zip file.")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
