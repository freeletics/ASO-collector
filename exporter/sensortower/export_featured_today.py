import logging
import moment
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils
from exporter.sensortower import export_featured_today

logger = logging.getLogger(__name__)

FEATURED_TODAY_IOS_ENDPOINT = "/ios/featured/today/stories"


def export_featured_today(exporter, export_from, export_to):
    executor = FeaturedTodayExecutor(exporter)
    executor.execute(export_from, export_to)


class FeaturedWriter(export_writer.ExportWriter):
    def get_row(self, key, data):
        date, country = key
        return {
            "date": date,
            "country": country,
            **{key: value for key, value in data.items()},
        }


class FeaturedTodayExecutor(utils.Executor):
    kpi = "featured_today"
    export_writer_class = FeaturedWriter
    apps = { config.SENSORTOWER_IOS_ID: config.PLATFORM_IOS }

    def write_export(self, data):
        self.write_export_for_platform(self.writer, data, "ios")

    def write_export_for_platform(self, writer, data, platform_name):
        filename_ios = self.get_filename(platform_name, self.kpi)
        writer.export_data(data, filename_ios, self.get_export_field_list())

    def get_proccessed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            date = moment.date(data["date"]).format(config.MOMENT_DATE_FORMAT)
            country = data["country"].lower()
            for story in data["stories"]:
                for index, app in enumerate(story["apps"]):
                    if config.FEATURED_TODAY_APP_NAME in app["name"]:
                        artwork = (
                            story["artwork"].get("url")
                            if story.get("artwork")
                            else None,
                        )
                        proccessed_data[(date, country)] = {
                            "app_name": app["name"],
                            "position": story["position"],
                            "title": story["title"],
                            "app_position": index,
                            "app_icon": app["icon_url"],
                            "artwork": artwork,
                        }
        return proccessed_data

    def get_export_field_list(self):
        return [
            "date",
            "country",
            "app_name",
            "position",
            "title",
            "app_position",
            "app_icon",
            "artwork",
        ]

    def get_export_data(self, params_list, exporter):
        exported_data = []
        for platform, params in params_list:
            data = exporter.request_data(FEATURED_TODAY_IOS_ENDPOINT, params)
            exported_data.extend(data)
        return exported_data

    def get_params(self, export_from, export_to, app_id, platform, country):
        return (
            platform,
            {
                "country": country.upper(),
                "start_date": export_from.strftime(config.DATE_FORMAT),
                "end_date": export_to.strftime(config.DATE_FORMAT),
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
            },
        )
