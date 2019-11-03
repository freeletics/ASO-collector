import logging
import moment
from exporter import config
from exporter.utils import export_writer
from exporter.sensortower import utils

logger = logging.getLogger(__name__)

REVIEW_ENDPOINT = "/{}/review/get_reviews"

REVIEWS_LIMIT = 200


def export_reviews(exporter, export_from, export_to):
    executor = ReviewExecutor(exporter)
    executor.execute(export_from, export_to)


class ReviewExecutor(utils.Executor):
    kpi = "reviews"
    key_template = "{}_star_{}"

    def get_proccessed_data(self, exported_data):
        proccessed_data = {}
        for data in exported_data:
            date = moment.date(data["date"]).format(config.MOMENT_DATE_FORMAT)
            platform = config.SENSORTOWER_APPS[str(data["app_id"])]
            country = data["country"].lower()
            rating = data["rating"]
            record = proccessed_data.setdefault(
                (date, platform), self.get_default_country_values()
            )
            record.update(
                    self.update_rate_counter(country, rating, record),
            )
            record.update(    {
                    f"{country}_average": self.get_average(country, rating, record),
                })

        return proccessed_data

    def get_export_field_list(self, countries):
        return [
            "date",
            *[f"{country}_average" for country in countries],
            *[
                f"{country}_star_{index}"
                for index in range(1, 6)
                for country in countries
            ],
        ]

    def get_average(self, country, rating, record):
        average = 0
        rating_count = sum([record[self.key_template.format(country, index)] for index in range(1,6)])
        for index in range(1, 6):
            average += record[self.key_template.format(country, index)] * index / rating_count
        return round(average, 2)

    def update_rate_counter(self, country, rating, record):
        key = self.key_template.format(country, rating)
        return {key: (record[key] + 1)}

    def get_default_country_values(self):
        return {
            **{f"{country}_average": None for country in config.COUNTRIES},
            **{
                f"{country}_star_{index}": 0
                for index in range(1, 6)
                for country in config.COUNTRIES
            },
        }

    def get_export_data(self, params_list, exporter):
        exported_data = []
        page_count = None
        for platform, params in params_list:
            page = 1
            while page_count is None or page <= page_count:
                params = {**params, "page": page}
                logger.info(
                    f"Getting data from review endpoint for params: {str(params)}"
                )
                data = exporter.request_data(REVIEW_ENDPOINT.format(platform), params)
                page_count = data["page_count"]
                page += 1
                exported_data.extend(data["feedback"])
        return exported_data

    def get_params(self, export_from, export_to, app_id, platform, country):
        return (
            platform,
            {
                "country": country,
                "app_id": app_id,
                "start_date": export_from.strftime(config.DATE_FORMAT),
                "end_date": export_to.strftime(config.DATE_FORMAT),
                "auth_token": config.SENSORTOWER_AUTH_TOKEN,
                "limit": REVIEWS_LIMIT,
            },
        )
