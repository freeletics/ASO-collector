import os
import logging
import moment
from datetime import datetime, timedelta
from exporter import config
from exporter import bucket
from exporter.utils import func
from exporter.utils import decorators
from exporter.play_store import script as play_store_script
from exporter.app_store import script as app_store_script
from exporter.apps_flyer import script as apps_flyier_script
from exporter.sensortower import script as sensortower_script
from exporter.app_follow import script as app_follow_script

logger = logging.getLogger(__name__)


def run(export_from, export_to):
    get_reports_from_s3_bucket()
    get_apps_flyier_export(export_from, export_to)
    get_app_follow_export(export_from, export_to)
    get_sensortower_export(export_from, export_to)
    get_play_store_export(export_from, export_to)
    get_app_store_export(export_from, export_to)


def get_reports_from_s3_bucket():
    if (
        config.GET_EXPORTS_FROM_BUCKET_BEFORE_RUN
        or len(os.listdir(config.EXPORTED_DATA_DIR)) == 0
    ):
        logger.info(f"No data present in exported data directory.")
        bucket_name = config.AWS_S3_BUCKET_NAME
        logger.info(f"Getting exported data reports from {bucket_name}")
        aws_bucket = bucket.BucketAws(bucket_name)
        for filepath in func.get_file_names_from_storage(aws_bucket):
            if not filepath.endswith("/"):
                func.download_file_from_storage(
                    aws_bucket, filepath, config.EXPORTED_DATA_DIR
                )


@decorators.catch_task_error("Play Store", logger)
def get_play_store_export(export_from, export_to):
    play_store_script.run(export_from, export_to)


@decorators.catch_task_error("App Store", logger)
def get_app_store_export(export_from, export_to):
    app_store_script.run(export_from, export_to)


@decorators.catch_task_error("Apps Flyier", logger)
def get_apps_flyier_export(export_from, export_to):
    apps_flyier_script.run(export_from, export_to)


@decorators.catch_task_error("Sensor Tower", logger)
def get_sensortower_export(export_from, export_to):
    sensortower_script.run(export_from, export_to)


@decorators.catch_task_error("App Follow", logger)
def get_app_follow_export(export_from, export_to):
    app_follow_script.run(export_from, export_to)


from exporter.utils import func

if __name__ == "__main__":
    func.run_script("Main", run)

