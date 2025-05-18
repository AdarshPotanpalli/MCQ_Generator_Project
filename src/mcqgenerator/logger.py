import logging
import os
from datetime import datetime

# file name for log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# folder where all the log files will be saved
log_path = os.path.join(os.getcwd(), "logs") # getcwd gets the current working directory
os.makedirs(log_path, exist_ok=True) # no error raised if the directory already present

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)


logging.basicConfig(
    level= logging.INFO, # level of logging
    filename= LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)