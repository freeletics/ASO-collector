import json
import copy
import logging
import moment
from datetime import datetime
from exporter import config
from exporter.utils import export_writer
from exporter.utils import context_managers
from exporter.utils import func
from exporter.sensortower import utils
from exporter.sensortower import export_featured_today

logger = logging.getLogger(__name__)

APP_UPDATES_TIMELINE_ENDPOINT = "/{}/app_update/get_app_update_history"


def export_versions(exporter, export_from):
    executor = AppUpdateTimelineExecutor(exporter)
    executor.execute(export_from)


class AppUpdateTimelineWriter(export_writer.ExportWriter):
    def get_row(self, key, data):
        date, country = key
        return {"date": date, **{key: value for key, value in data.items()}}

    def export_data(self, data, filename):
        data_copy = copy.copy(data)
        func.touch(filename)
        with context_managers.update_file(filename) as (old_file, temp_file):
            json.dump(data_copy, temp_file)
        self.files_saved.append(filename)


class AppUpdateTimelineExecutor(utils.Executor):
    kpi = "app_update_timeline"
    export_writer_class = AppUpdateTimelineWriter

    def write_export(self, data):
        filename = self.get_filename(data.pop("country"), data.pop("platform"))
        self.writer.export_data(data, filename)

    def get_filename(self, country, platform):
        return f"{config.EXPORTED_DATA_DIR}/{self.source_name}_{self.kpi}_{platform}_{country}_days.json"

    def execute(self, export_from):
        params_list = self.get_params_list(export_from)
        exported_data = self.get_export_data(params_list, self.exporter)
        processed_data = self.get_processed_data(exported_data)
        for data in processed_data:
            self.write_export(data)
        self.writer.upload_files()

    def get_processed_data(self, exported_data):
        logger.info(f"Processing versions timeline data")
        processed_data = []
        for change_data in exported_data:
            for data in change_data["update_data"]:
                update_data = data[1]
                update_data.pop("price", None)
                update_data.pop("support_url", None)
                update_data.pop("file_size", None)
                update_data.pop("related_app", None)
                update_data.pop("minimum_os_version", None)
                update_data.pop("featured_user_feedback", None)
                update_data.pop("install_range", None)
                update_data.pop("contains_ad", None)
                update_data.pop("top_in_app_purchase", None)
                update_data.pop("publisher_id", None)
                update_data.pop("keyword", None)
                update_data.pop("country", None)
                update_data.pop("supported_device", None)
                update_data.pop("supported_language", None)
                update_data.pop("apple_watch_enabled", None)
                update_data.pop("apple_watch_icon", None)
                update_data.pop("apple_watch_screenshot", None)
                update_data.pop("imessage_enabled", None)
                update_data.pop("imessage_icon", None)
            processed_data.append(change_data)
        return processed_data

    def get_export_data(self, params_list, exporter):
        exported_data = []
        for platform, country, params in params_list:
            logger.info(f"Getting versions data for params: {str(params)}")
            data = exporter.request_data(
                APP_UPDATES_TIMELINE_ENDPOINT.format(platform), params
            )
            data["platform"] = platform
            data["country"] = country
            exported_data.append(data)
        return exported_data

    def get_params(self, export_from, app_id, platform, country):
        delta = datetime.now() - export_from
        return (
            platform,
            country,
            {
                "country": country.upper(),
                "date_limit": delta.days,
                "app_id": app_id,
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
            },
        )

    def get_params_list(self, export_from):
        params_list = []
        for country in config.COUNTRIES:
            for app_id, platform in self.apps.items():
                params = self.get_params(export_from, app_id, platform, country)
                params_list.append(params)
        return params_list
