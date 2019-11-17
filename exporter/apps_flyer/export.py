import os
import csv
import requests
import logging

from exporter import config
from exporter.utils import executor

logger = logging.getLogger(__name__)

APPS_FLYER_MASTER_REPORT_ENDPOINT = "/export/master_report/v4"


class AppsFlyerExecutor(executor.Executor):
    source_name = "apps_flyer"
    kpi = "installs"
    kpis = "installs"
    groupings = "install_time,geo,af_channel"
    apps = config.APPS_FLYER_APPS
    file_name_template = "apps_flyer_installs_{platform}.csv"
    report_headers_map = {
        "Install Time": "date",
        "GEO": "country",
        "Channel": "channel",
        "Installs": "installs",
    }

    def raw_report_file(self, platform):
        return os.path.join(
            config.RAW_DATA_DIR, self.file_name_template.format(platform=platform)
        )

    def get_export_data(self, params_list, *args, **kwargs):
        export_data = []
        for platform, params in params_list:
            self.save_raw_report(platform, params)
            export_data.extend(self.read_raw_report(platform))
        return export_data

    def save_raw_report(self, platform, params):
        logger.info(f"Getting installs data for params: {str(params)}")
        response_data = self.exporter.request_data(
            APPS_FLYER_MASTER_REPORT_ENDPOINT, params
        )
        with open(
            self.raw_report_file(platform), "w", newline="", encoding="utf-8"
        ) as file:
            file.write(response_data)

    def read_raw_report(self, platform):
        raw_data = []
        with open(self.raw_report_file(platform), mode="r") as file:
            reader = csv.DictReader(file, fieldnames=self.report_headers_map.keys())
            next(reader)
            for row in reader:
                data = {
                    "platform": platform,
                    **{
                        key: row[csv_key]
                        for csv_key, key in self.report_headers_map.items()
                        if row.get(csv_key)
                    },
                }
                raw_data.append(data)
            return raw_data

    def get_proccessed_data(self, exported_data):
        logger.info(f"Processing installs data")
        proccessed_data = {}
        for data in exported_data:
            date = data["date"]
            platform = data["platform"]
            installs = data["installs"]
            country = data["country"].lower()
            record = proccessed_data.setdefault((date, platform), {})
            if data["channel"] == "None":
                record[f"{country}_organic"] = int(installs)
            else:
                paid = record.setdefault(f"{country}_paid", 0)
                record[f"{country}_paid"] = paid + int(installs)
        return proccessed_data

    def get_export_field_list(self, filed_list_params):
        return [
            "date",
            *self.get_country_fields("{}_organic"),
            *self.get_country_fields("{}_paid"),
        ]

    def get_country_fields(self, template):
        return [template.format(country) for country in config.COUNTRIES]

    def get_params(self, export_from, export_to, app_id, platform):
        return (
            platform,
            {
                "app_id": app_id,
                "api_token": config.APPS_FLYER_AUTH_TOKEN,
                "from": export_from.strftime(config.DATE_FORMAT),
                "to": export_to.strftime(config.DATE_FORMAT),
                "groupings": self.groupings,
                "kpis": self.kpis,
                "geo": ",".join([country.upper() for country in config.COUNTRIES]),
            },
        )

    def get_params_list(self, export_from, export_to):
        params_list = []
        for app_id, platform in self.apps.items():
            params = self.get_params(export_from, export_to, app_id, platform)
            params_list.append(params)
        return params_list


class AppsFlyerExport:
    def request_data(self, endpoint, params):
        response = self.get(endpoint, params)
        response.raise_for_status()
        return response.text

    def get(self, endpoint, params):
        return requests.get(
            f"{config.APPS_FLYER_ENDPOINT_BASE}{endpoint}", params=params
        )
