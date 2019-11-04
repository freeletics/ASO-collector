import os
import csv
import copy
from exporter import config
from exporter.utils import func
from exporter.utils import export_writer


class NoRawDataForPlayStore(Exception):
    pass


class PlayStoreExport(export_writer.ExportWriter):
    def __init__(
        self, source_data_filename, source_data_organic_filename, export_filename_base
    ):
        super().__init__()
        self.export_filename_base = export_filename_base
        self.source_data_filename = source_data_filename
        self.source_data_organic_filename = source_data_organic_filename
        self.raw_data_dir = config.RAW_DATA_DIR
        self.exported_data_dir = config.EXPORTED_DATA_DIR
        self.raw_data = []
        self.raw_data_organic = []
        self.raw_data_combined = {}
        self.downloads_organic = {}
        self.downloads_paid = {}
        self.page_views_organic = {}
        self.page_views_paid = {}
        self.convertion_rates_organic = {}
        self.convertion_rates_paid = {}

    def read_raw_data(self):
        self.read_raw_data_from_file(
            self.source_data_filename,
            self.raw_data,
            config.PLAY_STORE_CSV_HEADER_MAP_TOTAL,
        )
        for date, country, data in self.raw_data_generator(self.raw_data):
            self.raw_data_combined.setdefault(date, {})[country] = {
                "page_views": int(data["page_views"]),
                "downloads": int(data["downloads"]),
            }
        self.read_raw_data_from_file(
            self.source_data_organic_filename,
            self.raw_data_organic,
            config.PLAY_STORE_CSV_HEADER_MAP_ORGANIC,
        )
        for date, country, data in self.raw_data_generator(self.raw_data_organic):
            self.raw_data_combined.setdefault(date, {}).setdefault(country, {}).update(
                {
                    "page_views_organic": int(data["page_views_organic"]),
                    "downloads_organic": int(data["downloads_organic"]),
                }
            )

    def raw_data_generator(self, raw_data):
        for data in raw_data:
            date, country = self.get_date_country(data)
            yield date, country, data

    def read_raw_data_from_file(self, source_filename, raw_data, headers_map):
        file_path = os.path.join(self.raw_data_dir, source_filename)
        options = {"encoding": "utf-16"}
        try:
            self._read_raw_data(file_path, raw_data, headers_map, options)
        except UnicodeError:
            self._read_raw_data(file_path, raw_data, headers_map)
        except FileNotFoundError:
            raise NoRawDataForPlayStore(file_path)

    def _read_raw_data(self, file_path, raw_data, headers_map, options=None):
        options = options or {}
        with open(file_path, mode="r", **options) as file:
            reader = csv.DictReader(file)
            for raw in reader:
                data = {
                    key: raw[csv_key]
                    for csv_key, key in headers_map.items()
                    if raw.get(csv_key)
                }
                if data.get("country") and data["country"].lower() in config.COUNTRIES:
                    raw_data.append(data)

    def read_all(self):
        self.read_raw_data()
        self.read_downloads_organic()
        self.read_downloads_paid()
        self.read_page_views_organic()
        self.read_page_views_paid()
        self.read_convertion_rates_organic()
        self.read_convertion_rates_paid()

    def export_convertion_rates(self):
        self.export(self.convertion_rates_organic, "converstion_rates_organic")
        self.export(self.convertion_rates_paid, "converstion_rates_paid")

    def export_downloads(self):
        self.export(self.downloads_organic, "downloads_organic")
        self.export(self.downloads_paid, "downloads_paid")

    def export_page_views(self):
        self.export(self.page_views_organic, "page_views_organic")
        self.export(self.page_views_paid, "page_views_paid")

    def export(self, data, kpi_name):
        self.export_daily(data, kpi_name)

    def get_date_country(self, data):
        return data["date"], data["country"].lower()

    def read_downloads_organic(self):
        for date, country, data in self.data_generator():
            self.downloads_organic.setdefault(date, {})[country] = data.get(
                "downloads_organic", 0
            )

    def read_downloads_paid(self):
        for date, country, data in self.data_generator():
            self.downloads_paid.setdefault(date, {})[country] = data.get(
                "downloads", 0
            ) - data.get("downloads_organic", 0)

    def read_page_views_organic(self):
        for date, country, data in self.data_generator():
            self.page_views_organic.setdefault(date, {})[country] = data.get(
                "page_views_organic", 0
            )

    def read_page_views_paid(self):
        for date, country, data in self.data_generator():
            self.page_views_paid.setdefault(date, {})[country] = data.get(
                "page_views", 0
            ) - data.get("page_views_organic", 0)

    def read_convertion_rates_organic(self):
        for date, country, data in self.data_generator():
            self.convertion_rates_organic.setdefault(date, {})[
                country
            ] = func.convertion_rate(
                data.get("downloads_organic", 0), data.get("page_views_organic", 0)
            )

    def read_convertion_rates_paid(self):
        for date, country, data in self.data_generator():
            self.convertion_rates_paid.setdefault(date, {})[
                country
            ] = func.convertion_rate(
                data.get("downloads", 0) - data.get("downloads_organic", 0),
                data.get("page_views", 0) - data.get("page_views_organic", 0),
            )

    def data_generator(self):
        for date, countries_data in self.raw_data_combined.items():
            for country, data in countries_data.items():
                yield date, country, data

    def update_old_rows(self, writer, old_file, data):
        for row in csv.DictReader(old_file):
            try:
                date = row["date"]
                country_data = data.pop(date)
                writer.writerow(self.get_row(date, country_data))
            except KeyError:
                writer.writerow(
                    {
                        "date": row["date"],
                        **{
                            country: row[country]
                            for country in config.COUNTRIES
                            if row.get(country)
                        },
                    }
                )

    def get_row(self, date, data):
        return {
            "date": date,
            **{
                country: value
                for country, value in data.items()
                if country in config.COUNTRIES
            },
        }

    def export_daily(self, data, kpi_name):
        filename = self.get_export_filename(kpi_name, "days")
        self.export_data(data, filename, self.get_field_list())
        exported_data = self.get_exported_data(filename)
        return exported_data

    def get_exported_data(self, filename):
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            exported_data = {}
            for row in reader:
                exported_data[row["date"]] = row
            return exported_data

    def get_export_filename(self, kpi_name, aggregation):
        return os.path.join(
            self.exported_data_dir,
            f"{self.export_filename_base}_{kpi_name}_{aggregation}.csv",
        )

    @staticmethod
    def get_field_list():
        return ["date", *config.COUNTRIES]
