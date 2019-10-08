import os
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
EXPORTED_DATA_DIR = os.path.join(BASE_DIR, "exported_data")

LOG_FILE_NAME_DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(
    filename=f"logs/{datetime.now().strftime(LOG_FILE_NAME_DATE_FORMAT)}.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)
