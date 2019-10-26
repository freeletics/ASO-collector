import logging
from datetime import datetime, timedelta

from exporter import config
from exporter.apps_flyer import export

logger = logging.getLogger(__name__)

APPS_FLYER_ENDPOINT_BASE = "https://hq.appsflyer.com"

def run(export_from, export_to):
    exporter = export.AppsFlyerExport()
    executor = export.AppsFlyerExecutor(exporter)
    executor.execute(export_from, export_to)


if __name__ == "__main__":
    print("Exporting sensortower data")
    run(export_from=config.DEFAULT_EXPORT_FROM, export_to=datetime.now() - timedelta(days=1))
    print("Script finished")
