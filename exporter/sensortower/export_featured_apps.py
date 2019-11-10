import logging
import moment
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils
from exporter.sensortower import export_featured_today

logger = logging.getLogger(__name__)

FEATURED_TODAY_IOS_ENDPOINT = "/ios/featured/apps"


def export_featured_apps(exporter, export_from, export_to):
    executor = FeaturedAppsExecutor(exporter)
    executor.execute(export_from, export_to)


class FeaturedAppsExecutor(export_featured_today.FeaturedTodayExecutor):
    kpi = "featured_apps"
    aggregate = False

    def get_proccessed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            date = moment.date(data["date"]).format(config.MOMENT_DATE_FORMAT)
            country = data["country"].lower()
            for section in data["sections"]:
                for app in section["apps"]:
                    if (
                        app["name"] is not None
                        and config.FEATURED_TODAY_APP_NAME in app["name"]
                    ):
                        proccessed_data[(date, country)] = {
                            "app_name": app["name"],
                            "position": section["position"],
                            "title": section["title"],
                            "style": section["style"],
                            "app_icon": app["icon_url"],
                            "artwork": app["artwork_url"],
                        }
        return proccessed_data

    def get_export_field_list(self):
        return [
            "date",
            "country",
            "app_name",
            "position",
            "title",
            "style",
            "app_icon",
            "artwork",
        ]

    def get_export_data(self, params_list, exporter):
        exported_data = []
        for platform, params in params_list:
            data = exporter.request_data(FEATURED_TODAY_IOS_ENDPOINT, params)
            exported_data.extend(data)
        return exported_data

    def get_params(self, export_from, export_to, country, category):
        return (
            config.PLATFORM_IOS,
            {
                "country": country.upper(),
                "category": category,
                "start_date": export_from.strftime(config.DATE_FORMAT),
                "end_date": export_to.strftime(config.DATE_FORMAT),
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
            },
        )

    def get_params_list(self, export_from, export_to):
        params_list = []
        for country in config.COUNTRIES:
            for category in config.SENSORTOWER_FEATURED_APPS_IOS_CATEGORIES:
                params = self.get_params(export_from, export_to, country, category)
                params_list.append(params)
        return params_list
