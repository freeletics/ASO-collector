import logging
from datetime import datetime
from exporter import config
from exporter.play_store import script as play_store_script

logger = logging.getLogger(__name__)


def run():
    get_play_store_export()


def get_play_store_export():
    logger.info("Reading report from last run call")
    play_store_script.run(config.DEFAULT_EXPORT_FROM, datetime.now())
    logger.info("Task success")


if __name__ == "__main__":
    print("Running script")
    run()
    print("End of script")

