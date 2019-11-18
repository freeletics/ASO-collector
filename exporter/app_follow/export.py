import os
import csv
import requests
import logging
from hashlib import md5
from statistics import mean
from datetime import datetime
from datetime import timedelta

from exporter import config
from exporter.utils import executor

logger = logging.getLogger(__name__)

APP_FOLLOW_KEYWORDS = "/keywords"
APP_FOLLOW_ASO_SEARCH = "/aso/search"


class AppFollowKeywordExecutor(executor.Executor):
    source_name = "app_follow"
    kpi = "keywords"
    path = APP_FOLLOW_KEYWORDS
    apps = config.APP_FOLLOW_APPS

    @property
    def aggregate_func(self):
        return mean

    def get_export_data(self, params_list, exporter):
        export_data = []
        for platform, params in params_list:
            logger.info(f"Getting keywords for params: {str(params)}")
            data = exporter.request_data(APP_FOLLOW_KEYWORDS, params)
            export_data.extend(data["keywords"]["list"])
        return export_data

    def get_proccessed_data(self, exported_data):
        logger.info(f"Process keywords data")
        proccessed_data = {}
        for data in exported_data:
            platform = self.get_platform_for_device(data["device"])
            country = data["country"].lower()
            keyword = data["kw"]
            date = data["date"]
            pos = data["pos"]
            proccessed_data.setdefault((date, platform, country), {})[keyword] = int(
                pos
            )
        return proccessed_data

    def write_export(self, data):
        for (date, platform, country), keywords in data.items():
            filename = self.get_filename(platform, country, "days")
            field_list = self.get_export_field_list(keywords)
            self.writer.export_data({(date, platform): keywords}, filename, field_list)
            self.write_aggregated_exports(filename, field_list, platform, country)

    def get_export_field_list(self, keywords):
        return ["date", *keywords.keys()]

    def make_sign(self, path, params):
        sign = "{sorted_params}{path}{secret}".format(
            sorted_params="".join([f"{k}={params[k]}" for k in sorted(params.keys())]),
            path=path,
            secret=config.APP_FOLLOW_AUTH_TOKEN,
        )
        return md5(sign.encode()).hexdigest()

    def get_params(self, export_from, app_id, platform, country):
        params = {
            "cid": config.APP_FOLLOW_CID,
            "country": country,
            "ext_id": app_id,
            "date": export_from.strftime(config.DATE_FORMAT),
            "device": self.get_device_for_platform(platform),
        }
        sign = self.make_sign(self.path, params)
        return (platform, {**params, "sign": sign})

    def get_params_list(self, export_from, export_to):
        params_list = []
        while export_to - export_from > timedelta(days=0):
            for country in config.COUNTRIES:
                for app_id, platform in self.apps.items():
                    params = self.get_params(export_from, app_id, platform, country)
                    params_list.append(params)
            export_from = export_from + timedelta(days=1)
        return params_list

    def get_filename(self, platform, country, aggregate):
        return f"{config.EXPORTED_DATA_DIR}/{self.source_name}_{self.kpi}_{platform}_{country}_{aggregate}.csv"

    def get_device_for_platform(self, platform):
        return "android" if platform == config.PLATFORM_ANDROID else "iphone"

    def get_platform_for_device(self, device):
        return config.PLATFORM_ANDROID if device == "android" else config.PLATFORM_IOS


class AppFollowAsoSearchExecutor(AppFollowKeywordExecutor):
    source_name = "app_follow"
    kpi = "aso_search"
    path = APP_FOLLOW_ASO_SEARCH

    def execute(self):
        params_list = self.get_params_list()
        exported_data = self.get_export_data(params_list, self.exporter)
        processed_data = self.get_processed_data(exported_data)
        self.write_export(processed_data)
        self.writer.upload_files()

    def write_export(self, data):
        for (date, platform, country), keywords in data.items():
            filename = self.get_filename(platform, country, "days")
            field_list = self.get_export_field_list(keywords)
            self.writer.export_data({(date, platform): keywords}, filename, field_list)

    def get_params_list(self):
        params_list = []
        for country in config.COUNTRIES:
            for app_id, platform in self.apps.items():
                params = self.get_params(app_id, platform, country)
                params_list.append(params)
        return params_list

    def get_params(self, app_id, platform, country):
        params = {
            "cid": config.APP_FOLLOW_CID,
            "term": config.ASO_SEARCH_TERM,
            "country": country,
            "device": self.get_device_for_platform(platform),
        }
        sign = self.make_sign(self.path, params)
        return (country, {**params, "sign": sign})

    def get_export_data(self, params_list, exporter):
        export_data = []
        for country, params in params_list:
            logger.info(f"Getting ASO search for params: {str(params)}")
            data = exporter.request_data(APP_FOLLOW_ASO_SEARCH, params)
            for record in data["result"]:
                record["country"] = country
            export_data.extend(data["result"])
        return export_data

    def get_processed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            pos = data["pos"]
            if pos <= 10:
                platform = self.get_platform_for_device(data["device"])
                country = data["country"].lower()
                title = data["title"]
                date = datetime.now().strftime(config.DATE_FORMAT)
                proccessed_data.setdefault((date, platform, country), {})[
                    str(pos)
                ] = title
        return proccessed_data

    def get_export_field_list(self, keywords):
        return ["date", *[str(n) for n in range(1, 11)]]


class AppFollowExport:
    def request_data(self, endpoint, params):
        response = self.get(endpoint, params)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params):
        return requests.get(
            f"{config.APP_FOLLOW_ENDPOINT_BASE}{endpoint}", params=params
        )
