import pyodbc
import pandas as pd
import logging
from datetime import datetime
import os
from configparser import RawConfigParser
from setup_logging import *
import sys
from pathlib import Path
import os



current_directory = Path(os.getcwd()).resolve().parent
config_path = current_directory / 'config' / 'iconfig.ini'

config = RawConfigParser()
config.read(config_path)

# Set up logging for monitoring
setup_logging()

# Database connection parameters
server = config['SqlServer_Connection_Details']['server']
database = config['SqlServer_Connection_Details']['database']
# Table name
table_name = config['SqlServer_Connection_Details']['table_name']

# Connect to the database. This can be used for local machine.
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def table_exists(cursor, table_name):
    query = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
    cursor.execute(query)
    return cursor.fetchone() is not None

def create_table_if_not_exists(cursor, table_name):
    if not table_exists(cursor, table_name):
        create_query = f"""
        CREATE TABLE {table_name} (
            transaction_id INT PRIMARY KEY,
            city VARCHAR(50),
            transaction_date DATE,
            card_type VARCHAR(20),
            exp_type VARCHAR(20),
            gender CHAR(1),
            amount DECIMAL(10, 2)
        )
        """
        cursor.execute(create_query)
        conn.commit()
        logging.info(f"Table '{table_name}' created.")
    else:
        logging.info(f"Table '{table_name}' already exists.")

def is_unique(cursor, transaction_id, table_name):
    check_query = f"SELECT COUNT(1) FROM {table_name} WHERE transaction_id = ?"
    cursor.execute(check_query, transaction_id)
    return cursor.fetchone()[0] == 0

def insert_data(cursor, df, table_name):
    success_count = 0
    failed_ids = []

    for _, row in df.iterrows():
        if is_unique(cursor, row['transaction_id'], table_name):
            insert_query = f"""
            INSERT INTO {table_name} (transaction_id, city, transaction_date, card_type, exp_type, gender, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, row['transaction_id'], row['city'], row['transaction_date'],
                           row['card_type'], row['exp_type'], row['gender'], row['amount'])
            success_count += 1
        else:
            failed_ids.append(row['transaction_id'])

    return success_count, failed_ids

def log_failed_ids(failed_ids):
    if failed_ids:
        # Create a set to identify unique IDs and sort them
        unique_failed_ids = sorted(set(failed_ids))
        
        # Log ranges or individual IDs
        ranges = []
        start = unique_failed_ids[0]
        end = unique_failed_ids[0]

        for id in unique_failed_ids[1:]:
            if id == end + 1:  # If the ID is sequential
                end = id
            else:  # Otherwise, finalize the previous range
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = end = id
        
        # Add the last range or single ID
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")

        logging.info(f"The IDs {', '.join(ranges)} already exist in the table, hence skipping.")

# Main process
try:
    logging.info("#" * 50)
    logging.info("STEP 2 : Pushing the data to table")
    logging.info("#" * 50)
    create_table_if_not_exists(cursor, table_name)

    # Load DataFrame from the flow file (you may need to adjust this)
    df = pd.read_csv(sys.stdin)  # Example for reading from stdin in NiFi

    # Insert data and get the success count and failed IDs
    success_count, failed_ids = insert_data(cursor, df, table_name)
    conn.commit()

    # Log results
    logging.info(f"Data processing completed successfully. Total records pushed: {success_count}.")
    log_failed_ids(failed_ids)

except Exception as e:
    logging.error(f"Error processing data: {str(e)}")
finally:
    cursor.close()
    conn.close()
