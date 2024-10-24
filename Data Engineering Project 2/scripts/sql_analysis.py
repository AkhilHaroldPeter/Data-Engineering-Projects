import pyodbc
import pandas as pd
from read_sql_file import *
from configparser import RawConfigParser
from setup_logging import *
import sys
from pathlib import Path
import os

current_directory = Path(os.getcwd()).resolve().parent
config_path = current_directory / 'config' / 'iconfig.ini'
sql_files_path = current_directory / 'sql'

setup_logging()

# Load configuration
config = RawConfigParser()
config.read(config_path)

filename = sys.argv[1]

def sql_analysis(filename):
    # Check if the filename is valid
    if not filename.endswith('.sql'):
        logging.error("The provided file is not a valid SQL file.")
        return pd.DataFrame()  # Return empty DataFrame

    # Database connection parameters
    server = config['SqlServer_Connection_Details']['server']
    database = config['SqlServer_Connection_Details']['database']

    try:
        logging.info("#" * 50)
        logging.info("STEP 3 : Creating Reports")
        logging.info("#" * 50)    
        logging.info("Establishing database connection...")

        with pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;') as conn:
            logging.info("Database connection established successfully.")
            cursor = conn.cursor()

            # Read the SQL query from the file
            sql_query = read_sql_file(sql_files_path / filename)
            if sql_query is None:
                logging.error("Failed to retrieve SQL query from file: %s", filename)
                return pd.DataFrame()  # Return empty DataFrame on error            
            logging.info("SQL filename: %s", filename)
            logging.info("SQL query read from file: %s", sql_query)

            # Execute the SQL query and load data into a DataFrame
            df = pd.read_sql_query(sql_query, conn)
            logging.info("SQL query executed successfully. Retrieved %d rows.", len(df))
            df.to_csv(sys.stdout, index=False, header=True)
    
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return pd.DataFrame()  # Return empty DataFrame on error

    return df  # Return the DataFrame

sql_analysis(filename)
