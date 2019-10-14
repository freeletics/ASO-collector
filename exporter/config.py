import os
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
EXPORTED_DATA_DIR = os.path.join(BASE_DIR, "exported_data")

TASK_TRIES = 1

# Countries included in export
# TODO: update when final list known
COUNTRIES = ["ar", "es"]

DEFAULT_EXPORT_FROM = datetime(2018, 1, 1)

LOG_FILE_NAME_DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(
    filename=f"logs/{datetime.now().strftime(LOG_FILE_NAME_DATE_FORMAT)}.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)

# Play store
GCP_PLAY_STORE_REPORTS_BUCKET_NAME = os.environ["GCP_PLAY_STORE_REPORTS_BUCKET_NAME"]


PLAY_STORE_CSV_HEADER_MAP_BASE = {
    "Date": "date",
    "Country": "country",
    "Country (Play Store)": "country",
}

PLAY_STORE_CSV_HEADER_MAP_TOTAL = {
    **PLAY_STORE_CSV_HEADER_MAP_BASE,
    "Store Listing Visitors": "impressions",
    "Installers": "downloads",
}

PLAY_STORE_CSV_HEADER_MAP_ORGANIC = {
    **PLAY_STORE_CSV_HEADER_MAP_BASE,
    "Store Listing Visitors": "impressions_organic",
    "Installers": "downloads_organic",
}

PLAY_STORE_EXPORT_BASE_MAP = {"date": "date", "country": "country"}

PLAY_STORE_EXPORT_TOTAL_MAP = {**PLAY_STORE_EXPORT_BASE_MAP, "downloads": "downloads"}
