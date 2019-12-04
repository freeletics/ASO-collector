import logging
import moment
import datetime
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils
from exporter.sensortower import export_featured_today
from exporter.sensortower import categories

logger = logging.getLogger(__name__)

FEATURED_TODAY_CREATIVES = "/{}/featured/creatives"


def export_featured_creatives(exporter, export_from, export_to):
    executor = FeaturedCreativesExecutor(exporter)
    executor.execute(export_from, export_to)


class FeaturedCreativesExecutor(utils.Executor):
    kpi = "featured_creatives"
    export_writer_class = export_featured_today.FeaturedWriter
    aggregate = False

    def get_proccessed_data(self, exported_data):
        logger.info(f"Processing featured creatives data")
        proccessed_data = {}
        for data in exported_data:
            date = moment.date(data["positions"][0][0]).format(
                config.MOMENT_DATE_FORMAT
            )
            platform = data["platform"]
            position = data["positions"][0][1]
            country = data["country"].lower()
            path_list = [path_part for path_part in data.get("path", []) if path_part]
            path = "/".join(path_list)
            creatives_list = data.get("creatives", [])
            creatives = ",".join(creatives_list)
            category = categories.CATEGORIES[platform].get(str(data["category"]))
            type_ = data["type"]
            proccessed_data[(date, platform)] = {
                "country": country,
                "type": type_,
                "position": position,
                "path": path,
                "creatives": creatives,
                "category": category,
            }
        return proccessed_data

    def get_export_field_list(self, platform):
        return ["date", "country", "category", "type", "path", "creatives", "position"]

    def get_export_data(self, params_list, exporter):
        exported_data = []
        for platform, params in params_list:
            logger.info(f"Getting featured creatives data for params: {str(params)}")
            data = exporter.request_data(
                FEATURED_TODAY_CREATIVES.format(platform), params
            )
            platform_data = [
                {**featured, "platform": platform}
                for featured in data.get("features", [])
            ]
            exported_data.extend(platform_data)
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
            },
        )

    def get_params_list(self, export_from, export_to):
        params_list = []
        while export_to - export_from > datetime.timedelta(days=0):
            export_to_shorten = export_from + datetime.timedelta(days=config.FEATURED_MAX_RANGE)
            for app_id, platform in self.apps.items():
                params = self.get_params(export_from, export_to_shorten, app_id, platform)
                params_list.append(params)
            export_from = export_to_shorten
        return params_list
