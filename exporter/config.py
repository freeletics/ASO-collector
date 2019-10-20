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
# TODO: dodac skrypt do updatowania (ustawiania na null w csv) listy krajow
COUNTRIES = ["us", "de"]

DEFAULT_EXPORT_FROM = datetime(2019, 4, 1)

DATE_FORMAT = "%Y-%m-%d"
LOG_FILE_NAME_DATE_FORMAT = "%Y-%m-%d"
MOMENT_DATE_FORMAT = "YYYY-M-D"

logging.basicConfig(
    filename=f"logs/{datetime.now().strftime(LOG_FILE_NAME_DATE_FORMAT)}.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)

REQUEST_RETRIES = 3
REQUEST_RETRY_DELAY = 4

PLATFORM_IOS = "ios"
PLATFORM_ANDROID = "android"

# Sensor Tower
# TODO: ustalic max request (chyba 6 na sekunde)
SENSORTOWER_REQUEST_DELAY = 0.2

SENSORTOWER_AUTH_TOKEN = os.environ["SENSORTOWER_AUTH_TOKEN"]
SENSORTOWER_IOS_ID = os.environ["SENSORTOWER_IOS_ID"]
SENSORTOWER_ANDROID_ID = os.environ["SENSORTOWER_ANDROID_ID"]
SENSORTOWER_REQUEST_LIMIT = 200
SENSORTOWER_ENDPOINT_BASE = "https://api.sensortower.com/v1"

SENSORTOWER_APPS = {
    SENSORTOWER_IOS_ID: PLATFORM_IOS,
    SENSORTOWER_ANDROID_ID: PLATFORM_ANDROID,
}

SENSORTOWER_RANKING_CATEGORIES = {
    PLATFORM_IOS: ["0", "6013"],
    PLATFORM_ANDROID: ["application", "health_and_fitness"],
}

SENSORTOWER_RANKING_CHART_TYPES = {
    PLATFORM_IOS: ["topfreeapplications", "topfreeipadapplications"],
    PLATFORM_ANDROID: ["topselling_free"],
}

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
