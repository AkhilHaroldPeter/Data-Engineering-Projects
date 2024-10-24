# import logging
# from datetime import datetime
# from get_latest_log_file import *

# # Get the latest log file or create a new one
# def setup_logging():
#     latest_log_file = get_latest_log_file()
    
#     if latest_log_file:
#         # If there's an existing log file, append to it
#         logging.basicConfig(
#             filename=latest_log_file,
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s'
#         )
#         logging.info("Appending to existing log file.")
#     else:
#         # Create a new log file
#         today_date = datetime.now().strftime("%Y-%m-%d")
#         log_dir = os.path.join("LOGS", today_date)
#         os.makedirs(log_dir, exist_ok=True)
        
#         timestamp = datetime.now().strftime("%H-%M-%S")
#         new_log_file = os.path.join(log_dir, f"{today_date}_{timestamp}_data_ingestion.log")

#         logging.basicConfig(
#             filename=new_log_file,
#             level=logging.INFO,
#             format='%(asctime)s - %(levelname)s - %(message)s'
#         )
#         logging.info("Created new log file.")

import logging
import os
from datetime import datetime, timedelta
from get_latest_log_file import *

# Get the latest log file or create a new one
def setup_logging(is_session_log=False):
    if is_session_log:
        # Create a new log file for the session
        today_date = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join("LOGS", today_date)
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%H-%M-%S")
        new_log_file = os.path.join(log_dir, f"{today_date}_{timestamp}_session_log.log")

        logging.basicConfig(
            filename=new_log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Created new session log file.")
    else:
        # Get the latest log file
        latest_log_file = get_latest_log_file()
        
        if latest_log_file:
            # Check the modification time of the latest log file
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(latest_log_file))
            half_an_hour_ago = datetime.now() - timedelta(minutes=30)
            
            if file_mod_time > half_an_hour_ago:
                # If the log file exists and was created within the last half hour, append to it
                logging.basicConfig(
                    filename=latest_log_file,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                )
                logging.info("Appending to existing log file.")
            else:
                # Create a new log file since the existing one is older than half an hour
                today_date = datetime.now().strftime("%Y-%m-%d")
                log_dir = os.path.join("LOGS", today_date)
                os.makedirs(log_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%H-%M-%S")
                new_log_file = os.path.join(log_dir, f"{today_date}_{timestamp}_data_ingestion.log")

                logging.basicConfig(
                    filename=new_log_file,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                )
                logging.info("Created new log file.")
        else:
            # Create a new log file if none exists
            today_date = datetime.now().strftime("%Y-%m-%d")
            log_dir = os.path.join("LOGS", today_date)
            os.makedirs(log_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%H-%M-%S")
            new_log_file = os.path.join(log_dir, f"{today_date}_{timestamp}_data_ingestion.log")

            logging.basicConfig(
                filename=new_log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logging.info("Created new log file.")

# # Call this function when starting the "Generate Flow File" session
# def start_flow_file_session():
#     setup_logging(is_session_log=True)  # Pass True to create a new session log

# Example of usage
# Call start_flow_file_session() when you want to start a new session
# setup_logging() when logging other activities


