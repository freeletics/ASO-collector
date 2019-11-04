import logging
import os
from datetime import datetime
from datetime import date
from datetime import timedelta

from exporter import config
from exporter import bucket
from exporter.utils import decorators
from exporter.play_store import export

logger = logging.getLogger(__name__)


# TODO: download current state from AWS S3 bucket
@decorators.retry(Exception, tries=config.TASK_TRIES, logger=logger)
def run(export_from, export_to):
    logger.info("Getting Acquisition reports")
    bucket_name = config.GCP_PLAY_STORE_REPORTS_BUCKET_NAME
    logger.info(f"Connecting to GCP bucket {bucket_name}")
    play_store_bucket = bucket.BucketGcp(bucket_name)
    logger.info(f"Getting data starting from {export_from}")
    saved_files = download_reports(export_from, play_store_bucket)
    logger.info("Acquisition reports saved")
    logger.info("Updating export data")
    for date, monthly_data in saved_files.items():
        total_data_filename = monthly_data['total'] # TODO: jak wyjatek to zalogowac
        organic_data_filename = monthly_data['organic']
        logger.info(
            f"Reading data from files: {total_data_filename}, {organic_data_filename}"
        )
        exporter = export.PlayStoreExport(
            total_data_filename, organic_data_filename, "play_store"
        )
        exporter.read_all()
        logger.info("Exporting downloads")
        exporter.export_downloads()
        logger.info("Exporting convertsion rates")
        exporter.export_convertion_rates()
        logger.info("Exporting page_views")
        exporter.export_page_views()
        logger.info("Data updated")
        exporter.upload_files()
        logger.info("Upload data to s3 done")


def download_reports(export_from, bucket):
    saved_files = {}
    for filepath in get_file_names_from_storage(bucket):
        if not filepath.endswith("/") and report_download_condition(
            export_from, filepath
        ):
            download_file_from_storage(bucket, filepath)
            date = get_play_store_report_date(filepath).strftime("%Y-%m")
            filename = filepath.split("/")[-1]
            data_type = "organic" if "play_country" in filename else "total"
            saved_files.setdefault(date, {})[data_type] = filename
    return saved_files


def download_file_from_storage(bucket, file_name):
    logger.info(f"Getting file {file_name} from storage")
    bucket.download_file(file_name)


def get_file_names_from_storage(bucket):
    return [bucket.get_file_name(obj) for obj in bucket.get_all_objects()]


def report_download_condition(export_from, file_name):
    return export_from is None or get_play_store_report_date(
        file_name
    ) >= export_from - timedelta(days=30)


def get_play_store_report_date(name):
    try:
        return datetime.strptime(
            next((part for part in name.split("_") if part.isdigit())), "%Y%m"
        )
    except StopIteration:
        logger.info(
            f"File {name} do not have assumed format."
            "Update get_play_store_report_date function to properly extract date"
        )
        raise ValueError


# TODO: add ability to specify date range with args
if __name__ == "__main__":
    print("Exporting play store data")
    run(export_from=config.DEFAULT_EXPORT_FROM, export_to=datetime.now())
    print("Script finished")

