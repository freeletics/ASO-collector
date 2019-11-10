import logging
import moment
from statistics import mean
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils

logger = logging.getLogger(__name__)

RANKING_ENDPOINT = "/{}/category/category_history"


def export_rankings(exporter, export_from, export_to):
    executor = RankingExecutor(exporter)
    executor.execute(export_from, export_to)


class RankingExecutor(utils.Executor):
    kpi = "rankings"
    android_field_list_params = 'android'
    ios_field_list_params = 'ios'

    @property
    def aggregate_func(self):
        return mean

    def get_proccessed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            platform = config.SENSORTOWER_APPS[str(data["app_id"])]
            country = data["country"].lower()
            category = data["category"]
            chart_type = data["chart_type"]
            key = f"{country}_{category}_{chart_type}"
            for timestamp, ranking, _ in data["ranking_history"]:
                date = moment.unix(timestamp, utc=True).format(
                    config.MOMENT_DATE_FORMAT
                )
                proccessed_data.setdefault((date, platform), {})[key] = int(ranking)
        return proccessed_data

    def get_export_field_list(self, platform):
        field_list = ['date']
        for country in config.COUNTRIES:
            for category in config.SENSORTOWER_RANKING_CATEGORIES[platform]:
                for chart_type in config.SENSORTOWER_RANKING_CHART_TYPES[platform]:
                    field_list.append( f"{country}_{category}_{chart_type}")
        return field_list

    def get_export_data(self, params_list, exporter):
        exported_data = []
        for platform, params in params_list:
            logger.info(f"Getting data from ranking endpoint for params: {str(params)}")
            data = exporter.request_data(RANKING_ENDPOINT.format(platform), params)
            for app_id, country_data in data.items():
                if app_id in config.SENSORTOWER_APPS.keys():
                    for country, category_data in country_data.items():
                        for category, chart_type_data in category_data.items():
                            for chart_type, detail_data in chart_type_data.items():
                                exported_data.append(
                                    {
                                        "app_id": app_id,
                                        "country": country,
                                        "category": category,
                                        "chart_type": chart_type,
                                        "ranking_history": detail_data["graphData"],
                                    }
                                )
        return exported_data

    def get_params(self, export_from, export_to, app_id, platform):
        return (
            platform,
            {
                "countries": ",".join(config.COUNTRIES),
                "app_id": app_id,
                "start_date": export_from.strftime(config.DATE_FORMAT),
                "end_date": export_to.strftime(config.DATE_FORMAT),
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
                "categories": ",".join(config.SENSORTOWER_RANKING_CATEGORIES[platform]),
                "chart_type_ids": ",".join(
                    config.SENSORTOWER_RANKING_CHART_TYPES[platform]
                ),
            },
        )

    def get_params_list(self, export_from, export_to):
        params_list = []
        for app_id, platform in config.SENSORTOWER_APPS.items():
            params = self.get_params(export_from, export_to, app_id, platform)
            params_list.append(params)
        return params_list
