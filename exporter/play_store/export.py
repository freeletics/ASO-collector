import os
import csv
import copy
from exporter import config
from exporter.utils import context_managers
from exporter.utils import func


class NoRawDataForPlayStore(Exception):
    pass


class PlayStoreExport:
    def __init__(
        self, source_data_filename, source_data_organic_filename, export_filename_base
    ):
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
        self.convertion_rates_organic = {}
        self.convertion_rates_paid = {}
        self.files_saved = []

    def read_raw_data(self):
        self.read_raw_data_from_file(
            self.source_data_filename,
            self.raw_data,
            config.PLAY_STORE_CSV_HEADER_MAP_TOTAL,
        )
        for date, country, data in self.raw_data_generator(self.raw_data):
            self.raw_data_combined.setdefault(date, {})[country] = {
                "impressions": int(data["impressions"]),
                "downloads": int(data["downloads"]),
            }
        self.read_raw_data_from_file(
            self.source_data_organic_filename,
            self.raw_data_organic,
            config.PLAY_STORE_CSV_HEADER_MAP_ORGANIC,
        )
        for date, country, data in self.raw_data_generator(self.raw_data_organic):
            self.raw_data_combined.setdefault(date, {})[country].update(
                {
                    "impressions_organic": int(data["impressions_organic"]),
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
        self.read_convertion_rates_organic()
        self.read_convertion_rates_paid()

    def export_convertion_rates(self):
        self.export(self.convertion_rates_organic, "converstion_rates_organic", sum)
        self.export(self.convertion_rates_paid, "converstion_rates_paid", sum)

    def export_downloads(self):
        self.export(self.downloads_organic, "downloads_organic", sum)
        self.export(self.downloads_paid, "downloads_paid", sum)

    def export(self, data, kpi_name, aggregate_function):
        self.export_daily(data, kpi_name)

    def get_date_country(self, data):
        return data["date"], data["country"].lower()

    def read_downloads_organic(self):
        for date, country, data in self.data_generator():
            self.downloads_organic.setdefault(date, {})[country] = data[
                "downloads_organic"
            ]

    def read_downloads_paid(self):
        for date, country, data in self.data_generator():
            self.downloads_paid.setdefault(date, {})[country] = (
                data["downloads"] - data["downloads_organic"]
            )

    def read_convertion_rates_organic(self):
        for date, country, data in self.data_generator():
            self.convertion_rates_organic.setdefault(date, {})[
                country
            ] = self.calculate_convertion_rate(
                data["downloads_organic"], data["impressions_organic"]
            )

    def read_convertion_rates_paid(self):
        for date, country, data in self.data_generator():
            self.convertion_rates_paid.setdefault(date, {})[
                country
            ] = self.calculate_convertion_rate(
                data["downloads"] - data["downloads_organic"],
                data["impressions"] - data["impressions_organic"],
            )

    def data_generator(self):
        for date, countries_data in self.raw_data_combined.items():
            for country, data in countries_data.items():
                yield date, country, data

    def export_data(self, data, filename):
        data_copy = copy.copy(data)
        func.touch(filename)
        with context_managers.update_file(filename) as (old_file, temp_file):
            writer = csv.DictWriter(temp_file, fieldnames=self.get_field_list())
            writer.writeheader()
            self.update_old_rows(writer, old_file, data_copy)
            self.write_new_rows(writer, data_copy)
        self.sort_export_by_date(filename)
        self.files_saved.append(filename)

    def sort_export_by_date(self, filename):
        with context_managers.update_file(filename) as (old_file, temp_file):
            reader = csv.DictReader(old_file)
            sorted_rows = sorted(reader, key=lambda k: k["date"])
            writer = csv.DictWriter(temp_file, fieldnames=self.get_field_list())
            writer.writeheader()
            for row in sorted_rows:
                writer.writerow(row)

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

    def write_new_rows(self, writer, data):
        for date, country_data in data.items():
            writer.writerow(self.get_row(date, country_data))

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
        filename = self.get_export_filename(kpi_name, "daily")
        self.export_data(data, filename)
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

    @staticmethod
    def calculate_convertion_rate(downloads, impressions):
        try:
            return round(int(downloads) / int(impressions) * 100, 2)
        except ZeroDivisionError:
            return None
