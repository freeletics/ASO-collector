import logging
from datetime import datetime, timedelta

from exporter import config
from exporter.app_follow import export

logger = logging.getLogger(__name__)


def run(export_from, export_to):
    exporter = export.AppFollowExport()
    export.AppFollowAsoSearchExecutor(exporter).execute()
    export.AppFollowKeywordExecutor(exporter).execute(export_from, export_to)


if __name__ == "__main__":
    print("Exporting app follow data")
    run(export_from=config.DEFAULT_EXPORT_FROM, export_to=datetime.now() - timedelta(days=1))
    print("Script finished")
