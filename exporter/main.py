import logging
import moment
from datetime import datetime, timedelta
import fire
from exporter import config
from exporter.play_store import script as play_store_script
from exporter.app_store import script as app_store_script
from exporter.apps_flyer import script as apps_flyier_script
from exporter.sensortower import script as sensortower_script


logger = logging.getLogger(__name__)


def string_to_date(date):
    return moment.date(date) if date else None


def run(export_from=None, export_to=None):
    export_from = string_to_date(export_from) or config.DEFAULT_EXPORT_FROM
    export_to = string_to_date(export_to) or datetime.now() - timedelta(days=1)
    logger.info(f"Exporting data from {export_from} to {export_to}")
    get_apps_flyier_export(export_from, export_to)
    get_sensortower_export(export_from, export_to)
    get_play_store_export(export_from, export_to)
    get_app_store_export(export_from, export_to)


def get_play_store_export(export_from, export_to):
    try:
        logger.info("Play Store task")
        play_store_script.run(export_from, export_to)
    except Exception:
        logger.error("Play Store task failed ")


def get_app_store_export(export_from, export_to):
    try:
        logger.info("App Store task")
        app_store_script.run(export_from, export_to)
    except Exception:
        logger.error("App Store task failed ")


def get_apps_flyier_export(export_from, export_to):
    try:
        logger.info("Apps Flyier task")
        apps_flyier_script.run(export_from, export_to)
    except Exception:
        logger.error("Apps Flyier task failed ")


def get_sensortower_export(export_from, export_to):
    try:
        logger.info("Sensor Tower task")
        sensortower_script.run(export_from, export_to)
    except Exception:
        logger.error("Sensor Tower task failed ")


if __name__ == "__main__":
    print("Running script")
    fire.Fire(run)
    print("End of script")

