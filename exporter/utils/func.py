import os
import sys
import csv
import moment
import logging
from datetime import datetime
from datetime import timedelta
from exporter import config

logger = logging.getLogger(__name__)


def touch(filename):
    with open(filename, "a"):
        os.utime(filename, None)


def get_last_date(export_from, filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            return max([moment.date(row["date"]).date for row in reader])
    except (ValueError, FileNotFoundError):
        return export_from


def convertion_rate(downloads, denominator):
    try:
        return round(int(downloads) / int(denominator) * 100, 2)
    except ZeroDivisionError:
        return None


def download_file_from_storage(bucket, file_name, download_to=None):
    logger.info(f"Getting file {file_name} from storage")
    bucket.download_file(file_name, download_to)


def get_file_names_from_storage(bucket):
    return [bucket.get_file_name(obj) for obj in bucket.get_all_objects()]


def string_to_date(date):
    return moment.date(date) if date else None


def run_script(name, script_run):
    print(f"Running script {name}")
    logger.info(f"Running script {name}")
    export_from = string_to_date(sys.argv[1]) if sys.argv == 2 else config.DEFAULT_EXPORT_FROM
    export_to = string_to_date(export_to) if sys.argv == 3 else config.DEFAULT_EXPORT_TO
    logger.info(f"Exporting data from {export_from} to {export_to}")
    script_run(export_from, export_to)
    logger.info(f"End of script {name}")
    print(f"End of script {name}")