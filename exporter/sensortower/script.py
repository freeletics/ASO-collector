import logging
from datetime import datetime

from exporter import config
from exporter.utils import decorators
from exporter.sensortower import export
from exporter.sensortower import export_ratings
from exporter.sensortower import export_rankings
from exporter.sensortower import export_reviews

logger = logging.getLogger(__name__)


@decorators.retry(Exception, tries=config.TASK_TRIES, logger=logger)
def run(export_from, export_to):
    exporter = export.SensorTowerExport()
    logger.info("Getting ratings reports")
    export_ratings.export_ratings(exporter, export_from, export_to)
    logger.info("Getting reviews reports")
    export_reviews.export_reviews(exporter, export_from, export_to)
    logger.info("Getting rankings reports")
    export_rankings.export_rankings(exporter, export_from, export_to)
    logger.info(f"Sensortower API calls count: {exporter.request_counter}")

if __name__ == "__main__":
    print("Exporting sensortower data")
    run(export_from=config.DEFAULT_EXPORT_FROM, export_to=datetime.now())
    print("Script finished")
