import logging
from datetime import datetime

from exporter import config
from exporter.utils import decorators
from exporter.sensortower import export
from exporter.sensortower import export_ratings

logger = logging.getLogger(__name__)


@decorators.retry(Exception, tries=config.TASK_TRIES, logger=logger)
def run(export_from, export_to):
    exporter = export.SensorTowerExport()
    logger.info("Getting ratings reports")
    export_ratings.export_ratings(exporter, export_from, export_to)


if __name__ == "__main__":
    print("Exporting sensortower data")
    run(export_from=config.DEFAULT_EXPORT_FROM, export_to=datetime.now())
    print("Script finished")