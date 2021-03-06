import os
from datetime import datetime
from datetime import timedelta
import moment
import logging
from dotenv import load_dotenv

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

load_dotenv(os.path.join(BASE_DIR, '.env'))

RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
EXPORTED_DATA_DIR = os.path.join(BASE_DIR, "exported_data")
APP_STORE_NODE_APP_DIR = os.path.join(BASE_DIR, "exporter/app_store_node")

DEBUG = os.environ.get("DEBUG", False)
TASK_TRIES = 1 if DEBUG else 3
GET_EXPORTS_FROM_BUCKET_BEFORE_RUN = int(os.environ.get("GET_EXPORTS_FROM_BUCKET_BEFORE_RUN", 1))
OPTIMIZE_EXPORT_FROM = int(os.environ.get('OPTIMIZE_EXPORT_FROM', 1))

# Countries included in export
COUNTRIES = ["us", "de", "gb", "fr", "it"]

DEFAULT_EXPORT_TO = datetime.now() - timedelta(days=3)
DEFAULT_EXPORT_FROM = moment.date(os.environ["DEFAULT_EXPORT_FROM"]).date
DEFAULT_EXPORT_FROM = DEFAULT_EXPORT_FROM if DEFAULT_EXPORT_TO - DEFAULT_EXPORT_FROM > timedelta(days=0) else DEFAULT_EXPORT_TO

DATE_FORMAT = "%Y-%m-%d"
LOG_FILE_NAME_DATE_FORMAT = "%Y-%m-%d"
MOMENT_DATE_FORMAT = "YYYY-M-D"

logging.basicConfig(
    filename=f"{BASE_DIR}/logs/{datetime.now().strftime(LOG_FILE_NAME_DATE_FORMAT)}.log",
    level=logging.INFO,
    filemode="a",
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)

AWS_S3_BUCKET_NAME = os.environ["AWS_S3_BUCKET_NAME"]

REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 3
REQUEST_RETRY_DELAY = 4

PLATFORM_IOS = "ios"
PLATFORM_ANDROID = "android"

# App Follow
APP_FOLLOW_AUTH_TOKEN = os.environ["APP_FOLLOW_AUTH_TOKEN"]
APP_FOLLOW_CID = os.environ["APP_FOLLOW_CID"]
APP_FOLLOW_IOS_ID = os.environ["APP_FOLLOW_IOS_ID"]
APP_FOLLOW_ANDROID_ID = os.environ["APP_FOLLOW_ANDROID_ID"]
APP_FOLLOW_ENDPOINT_BASE = "http://api.appfollow.io"
ASO_SEARCH_TERM = os.environ['ASO_SEARCH_TERM']

APP_FOLLOW_APPS = {
    APP_FOLLOW_IOS_ID: PLATFORM_IOS,
    APP_FOLLOW_ANDROID_ID: PLATFORM_ANDROID,
}

# Apps Flyer
APPS_FLYER_AUTH_TOKEN = os.environ["APPS_FLYER_AUTH_TOKEN"]
APPS_FLYER_IOS_ID = os.environ["APPS_FLYER_IOS_ID"]
APPS_FLYER_ANDROID_ID = os.environ["APPS_FLYER_ANDROID_ID"]
APPS_FLYER_ENDPOINT_BASE = "https://hq.appsflyer.com"

APPS_FLYER_APPS = {
    APPS_FLYER_IOS_ID: PLATFORM_IOS,
    APPS_FLYER_ANDROID_ID: PLATFORM_ANDROID,
}

# App Store
APP_STORE_USERNAME = os.environ["APP_STORE_USERNAME"]
APP_STORE_PASSWORD = os.environ["APP_STORE_PASSWORD"]
APP_STORE_APP_ID = os.environ["APP_STORE_APP_ID"]
SEARCH_ADS_CERTIFICATES = os.environ["SEARCH_ADS_CERTIFICATES"]
APP_STORE_RAW_DATA_FILENAME = "app_store_data.json"
SEARCH_ADS_ONLY = os.environ.get("SEARCH_ADS_ONLY", False)

# Sensor Tower
SENSORTOWER_REQUEST_DELAY = 0.2

SENSORTOWER_AUTH_TOKEN = os.environ["SENSORTOWER_AUTH_TOKEN"]
SENSORTOWER_IOS_ID = os.environ["SENSORTOWER_IOS_ID"]
SENSORTOWER_ANDROID_ID = os.environ["SENSORTOWER_ANDROID_ID"]
SENSORTOWER_REQUEST_LIMIT = 200
SENSORTOWER_ENDPOINT_BASE = "https://api.sensortower.com/v1"

FEATURED_TODAY_APP_NAME = os.environ["FEATURED_TODAY_APP_NAME"]
FEATURED_MAX_RANGE = 30

# ALL CATEGORIES SPECIFIED IN exporter/sensortower/categories.py
SENSORTOWER_FEATURED_APPS_IOS_CATEGORIES = ["6013"]

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
PLAY_STORE_APP_ID = os.environ.get("PLAY_STORE_APP_ID", "com.freeletics.lite")

PLAY_STORE_CSV_HEADER_MAP_BASE = {
    "Date": "date",
    "Country": "country",
    "Country (Play Store)": "country",
}

PLAY_STORE_CSV_HEADER_MAP_TOTAL = {
    **PLAY_STORE_CSV_HEADER_MAP_BASE,
    "Store Listing Visitors": "page_views",
    "Installers": "downloads",
}

PLAY_STORE_CSV_HEADER_MAP_ORGANIC = {
    **PLAY_STORE_CSV_HEADER_MAP_BASE,
    "Store Listing Visitors": "page_views_organic",
    "Installers": "downloads_organic",
}

PLAY_STORE_EXPORT_BASE_MAP = {"date": "date", "country": "country"}

PLAY_STORE_EXPORT_TOTAL_MAP = {**PLAY_STORE_EXPORT_BASE_MAP, "downloads": "downloads"}
