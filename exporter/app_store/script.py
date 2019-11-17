import os
import json
import logging
from datetime import datetime

from exporter import config
from exporter.utils import func
from exporter.utils import decorators
from exporter.app_store import export
from Naked.toolshed.shell import execute_js

logger = logging.getLogger(__name__)


CHECK_LAST_DATE_FILE = os.path.join(
    config.EXPORTED_DATA_DIR, "app_store_conversion_rates_days.csv"
)
APP_STORE_RAW_DATA_FILE = os.path.join(
    config.RAW_DATA_DIR, config.APP_STORE_RAW_DATA_FILENAME
)


class AppStoreScriptFailed(Exception):
    ...


# TODO: dodac logowanie ze skryptu
@decorators.retry(AppStoreScriptFailed, tries=config.TASK_TRIES, logger=logger)
def run(export_from, export_to):
    if config.OPTIMIZE_EXPORT_FROM:
        export_from = func.get_last_date(export_from, CHECK_LAST_DATE_FILE)
    success = execute_js(
        os.path.join(config.APP_STORE_NODE_APP_DIR, "index.js"),
        arguments=build_arguments(export_from, export_to),
    )
    if not success:
        raise AppStoreScriptFailed
    with open(APP_STORE_RAW_DATA_FILE) as json_file:
        data = json.load(json_file)
        exporter = export.AppStoreExport()
        exporter.proccessed_data(data)
        exporter.write_exports()
        exporter.writer.upload_files()


def build_arguments(export_from, export_to):
    options = {
        "username": config.APP_STORE_USERNAME,
        "password": config.APP_STORE_PASSWORD,
        "export_from": export_from.strftime(config.DATE_FORMAT),
        "export_to": export_to.strftime(config.DATE_FORMAT),
        "raw_output": APP_STORE_RAW_DATA_FILE,
        "certificates": config.SEARCH_ADS_CERTIFICATES,
        "app_id": config.APP_STORE_APP_ID,
        "search_ads_only": 1 if config.SEARCH_ADS_ONLY else 0,
    }
    return """--username '{username}' \
              --password '{password}' \
              --id '{app_id}' \
              --from '{export_from}' \
              --to '{export_to}' \
              --output '{raw_output}' \
              --certificates '{certificates}' \
              --search_ads_only '{search_ads_only}'
           """.format(
        **options
    )


if __name__ == "__main__":
    func.run_script("App Store and Search Ads", run)

