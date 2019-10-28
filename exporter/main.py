import logging
from datetime import datetime
from exporter import config
from exporter.play_store import script as play_store_script
from exporter.app_store import script as app_store_script
from exporter.apps_flyer import script as apps_flyier_script
from exporter.sensortower import script as sensortower_script


logger = logging.getLogger(__name__)


def run():
    get_play_store_export()
    get_app_store_export()
    get_apps_flyier_export()
    get_sensortower_export()


def get_play_store_export():
    logger.info("Play Store task")
    play_store_script.run(config.DEFAULT_EXPORT_FROM, datetime.now())


def get_app_store_export():
    logger.info("App Store task")
    app_store_script.run(config.DEFAULT_EXPORT_FROM, datetime.now())


def get_apps_flyier_export():
    logger.info("Apps Flyier task")
    apps_flyier_script.run(config.DEFAULT_EXPORT_FROM, datetime.now())


def get_sensortower_export():
    logger.info("Sensor Tower task")
    sensortower_script.run(config.DEFAULT_EXPORT_FROM, datetime.now())


if __name__ == "__main__":
    print("Running script")
    run()
    print("End of script")

