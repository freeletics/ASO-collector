import logging
from datetime import datetime, timedelta

from exporter import config
from exporter.utils import func
from exporter.app_follow import export

logger = logging.getLogger(__name__)


def run(export_from, export_to):
    exporter = export.AppFollowExport()
    logger.info("Getting ASO Search data")
    export.AppFollowAsoSearchExecutor(exporter).execute()
    logger.info("Getting Keywords data")
    export.AppFollowKeywordExecutor(exporter).execute(export_from, export_to)
    logger.info("Getting Rating data")
    export.AppFollowRatingExecutor(exporter).execute(export_from, export_to)

if __name__ == "__main__":
    func.run_script('App Follow', run)

