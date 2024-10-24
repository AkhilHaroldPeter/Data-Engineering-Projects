import pyodbc
import pandas as pd
from read_sql_file import *
from configparser import RawConfigParser
from setup_logging import *
import sys
from pathlib import Path
import os
# from datetime import datetime



current_directory = Path(os.getcwd()).resolve().parent
config_path = current_directory / 'config' / 'iconfig.ini'
sql_files_path = current_directory / 'sql'

setup_logging()

# Load configuration
config = RawConfigParser()
config.read(config_path)

filename = sys.argv[1]

#'Top 5 Expense Categories.sql'
def sql_analysis(filename):
    # Set up logging for monitoring
    

    # Database connection parameters
    server = config['SqlServer_Connection_Details']['server']
    database = config['SqlServer_Connection_Details']['database']

    try:
        logging.info(f"#"*50)
        logging.info(f"STEP 3 : Creating Reports")
        logging.info(f"#"*50)    
        logging.info("Establishing database connection...")
        # Connect to the database
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(conn_str)
        logging.info("Database connection established successfully.")

        cursor = conn.cursor()

        # Read the SQL query from the file
        sql_query = read_sql_file(sql_files_path / filename)
        logging.info("SQL filename: %s", filename)
        logging.info("SQL query read from file: %s", sql_query)

        # Execute the SQL query and load data into a DataFrame
        df = pd.read_sql_query(sql_query, conn)
        logging.info("SQL query executed successfully. Retrieved %d rows.", len(df))
        df.to_csv(sys.stdout, index=False, header=True)
    except Exception as e:
        logging.error("An error occurred: %s", e)

    finally:
        # Ensure the database connection is closed
        if cursor:
            cursor.close()
            logging.info("Cursor closed.")
        if conn:
            conn.close()
            logging.info("Database connection closed.")
    return df  # Return the DataFrame
sql_analysis(filename)