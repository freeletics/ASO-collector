import logging
from datetime import datetime, timedelta

from exporter import config
from exporter.utils import func
from exporter.apps_flyer import export

logger = logging.getLogger(__name__)


def run(export_from, export_to):
    exporter = export.AppsFlyerExport()
    executor = export.AppsFlyerExecutor(exporter)
    executor.execute(export_from, export_to)


if __name__ == "__main__":
    func.run_script("Apps Flyer", run)

