import logging
from setup_logging import *
setup_logging()

def read_sql_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            sql_query = file.read()
            logging.info("Successfully read SQL file: %s", filename)
            return sql_query
    except FileNotFoundError:
        logging.error("SQL file not found: %s", filename)
        return None  # Return None or raise an exception based on your needs
    except Exception as e:
        logging.error("An error occurred while reading SQL file: %s. Error: %s", filename, str(e))
        return None  # Return None or raise an exception based on your needs
