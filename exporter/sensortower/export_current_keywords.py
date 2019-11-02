import logging
from datetime import datetime
import moment
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils

logger = logging.getLogger(__name__)

CURRENT_KEYWORDS_ENDPOINT = "/{}/keywords/get_current_keywords"


def export_current_keywords(exporter):
    executor = KeywordsExecutor(exporter)
    executor.execute()


class KeywordsExecutor(utils.Executor):
    kpi = "current_keywords"

    def write_export(self, data):
        for (date, platform, country), keywords in data.items():
            filename = self.get_filename(country, platform)
            self.writer.export_data(
                {(date, platform): keywords},
                filename,
                self.get_export_field_list(keywords),
            )

    def execute(self):
        params_list = self.get_params_list()
        exported_data = self.get_export_data(params_list, self.exporter)
        processed_data = self.get_processed_data(exported_data)
        self.write_export(processed_data)
        self.writer.upload_files()

    def get_filename(self, platform, country):
        return f"{config.EXPORTED_DATA_DIR}/{self.source_name}_{self.kpi}_{platform}_{country}_days.csv"

    def get_processed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            date = datetime.now().strftime(config.DATE_FORMAT)
            platform = data["platform"]
            country = data["country"]
            proccessed_data[(date, platform, country)] = self.get_keywords(data["keywords"])
        return proccessed_data

    def get_keywords(self, keywords):
        return {keyword["term"]: keyword["rank"] for keyword in keywords}

    def get_export_field_list(self, keywords):
        return ["date", *keywords.keys()]

    def get_export_data(self, params_list, exporter):
        exported_data = []
        page_count = None
        for platform, country, params in params_list:
            data = exporter.request_data(
                CURRENT_KEYWORDS_ENDPOINT.format(platform), params
            )
            exported_data.append(
                {"keywords": data["keywords"], "platform": platform, "country": country}
            )
        return exported_data

    def get_params(self, app_id, platform, country):
        return (
            platform,
            country,
            {
                "country": country,
                "app_id": app_id,
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
            },
        )

    def get_params_list(self):
        params_list = []
        for country in config.COUNTRIES:
            for app_id, platform in self.apps.items():
                params = self.get_params(app_id, platform, country)
                params_list.append(params)
        return params_list
