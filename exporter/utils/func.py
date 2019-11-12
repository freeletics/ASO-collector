import os
import csv
import moment
import logging

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
