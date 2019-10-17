import logging
import moment
from exporter import config
from exporter.utils import export_writer

logger = logging.getLogger(__name__)

RATING_ENDPOINT = "/{}/review/get_ratings"
MOMENT_DATE_FORMAT = "YYYY-M-D"

# TODO: sprawdzic poprawnosc danych dla ios (brakujace dni)
# TODO: aggregacja export
# TODO: dodac logowanie
def export_ratings(exporter, export_from, export_to):
    params_list = get_params_list(export_from, export_to)
    exported_data = get_export_data(params_list, exporter)
    proccessed_data = get_proccessed_data(exported_data)
    write_export(proccessed_data)


def write_export(data):
    writer = export_writer.ExportWriter()
    write_export_for_platform(writer, data, "ios", config.COUNTRIES)
    write_export_for_platform(writer, data, "android", ["global"])


def write_export_for_platform(writer, data, platform_name, countries):
    filename_ios = get_filename(platform_name)
    filtered_data = filter_data_for_platform(data, platform_name)
    writer.export_data(filtered_data, filename_ios, get_export_field_list(countries))


def get_filename(platform_name):
    return f"{config.EXPORTED_DATA_DIR}/sensortower_ratings_{platform_name}_daily.csv"


def filter_data_for_platform(data, platform_name):
    return {
        (date, platform): value
        for (date, platform), value in data.items()
        if platform == platform_name
    }


def get_export_field_list(countries):
    return [
        "date",
        *[f"{country}_average" for country in countries],
        *[f"{country}_star_{index}" for index in range(1, 6) for country in countries],
    ]


def get_proccessed_data(exported_data):
    data = get_row_per_date(exported_data)
    proccessed_data = get_calculated_daily_amounts(data)
    return proccessed_data


def get_row_per_date(exported_data):
    proccessed_data = {}
    for data in exported_data:
        date = moment.date(data["date"]).format(MOMENT_DATE_FORMAT)
        platform = config.SENSORTOWER_APPS[str(data["app_id"])]
        country = data["country"].lower() if platform == "ios" else "global"
        proccessed_data.setdefault((date, platform), {}).update(
            {
                f"{country}_average": data["average"],
                f"{country}_star_1": data["breakdown"][0],
                f"{country}_star_2": data["breakdown"][1],
                f"{country}_star_3": data["breakdown"][2],
                f"{country}_star_4": data["breakdown"][3],
                f"{country}_star_5": data["breakdown"][4],
            }
        )
    return proccessed_data


def get_calculated_daily_amounts(proccessed_data):
    rows_to_drop = []
    for (date, platform), data in proccessed_data.items():
        try:
            yesterday = moment.date(date).subtract(days=1).format(MOMENT_DATE_FORMAT)
            for country in config.COUNTRIES if platform == "ios" else ["global"]:
                proccessed_data[(date, platform)].update(
                    {
                        get_rating_star_cell(
                            country, index, data, proccessed_data[(yesterday, platform)]
                        )
                        for index in range(1, 6)
                    }
                )
        except KeyError:
            rows_to_drop.append((date, platform))
    for date, platform in rows_to_drop:
        del proccessed_data[(date, platform)]
    return proccessed_data


def get_rating_star_cell(country, start_index, sub_from, sub_what):
    key = f"{country}_star_{start_index}"
    return key, substract_keys(key, sub_from, sub_what)


def substract_keys(key, sub_from, sub_what):
    return int(sub_from[key]) - int(sub_what[key])


def get_export_data(params_list, exporter):
    exported_data = []
    for platform, params in params_list:
        logger.info(f"Getting data from rating endpoint for params: {str(params)}")
        data = exporter.request_data(RATING_ENDPOINT.format(platform), params)
        exported_data.extend(data)
        logger.info(f"Data from rating endpoint: {str(data)}")
    return exported_data


def get_params_list(export_from, export_to):
    params_list = []
    for country in config.COUNTRIES:
        for app_id, platform in config.SENSORTOWER_APPS.items():
            params = get_params(export_from, export_to, app_id, platform, country)
            params_list.append(params)
    return params_list


def get_params(export_from, export_to, app_id, platform, country):
    country = {"country": country} if platform == "ios" else {}
    return (
        platform,
        {
            **country,
            "app_id": app_id,
            "start_date": export_from.strftime(config.DATE_FORMAT),
            "end_date": export_to.strftime(config.DATE_FORMAT),
            "auth_token": config.SENSORTOWER_AUTH_TOKEN,
        },
    )

