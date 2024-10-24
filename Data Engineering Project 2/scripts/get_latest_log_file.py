import os
from datetime import datetime
from pathlib import Path
import os

current_directory = Path(os.getcwd()).resolve().parent
log_path = current_directory / 'data' / 'LOGS' 

def get_latest_log_file():
    # Define the path for today's log directory
    today_date = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(log_path, today_date)

    # Create the directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Get all log files in the directory
    log_files = [logfile for logfile in os.listdir(log_dir) if logfile.endswith('.log')]
    
    # If there are no log files, return None
    if not log_files:
        return None

    # Get the full path of the most recently created log file
    latest_log_file = max(
        [os.path.join(log_dir, f) for f in log_files],
        key=os.path.getctime
    )
    
    return latest_log_file
