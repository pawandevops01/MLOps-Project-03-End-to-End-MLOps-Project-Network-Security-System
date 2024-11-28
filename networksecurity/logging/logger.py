import logging
import os
from datetime import datetime


# Create logs directory if it doesn't exist
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

# Define a single log file
LOG_FILE = "network_security_logs.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# -----------------------------------------------------
#  Old code as per course
# -----------------------------------------------------
# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# os.makedirs(logs_path, exist_ok=True)
# LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
# -----------------------------------------------------

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] - line_number: %(lineno)d - module: %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

