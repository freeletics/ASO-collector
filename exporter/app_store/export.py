import os
import csv
from itertools import chain

from exporter import config
from exporter.utils import func
from exporter.utils import export_writer


class AppStoreExportWriter(export_writer.ExportWriter):
    def get_key(self, row):
        return row["date"]

    def get_row(self, date, data):
        return {"date": date, **{key: value for key, value in data.items()}}

    def update_old_rows(self, writer, old_file, data):
        for row in csv.DictReader(old_file):
            try:
                key = self.get_key(row)
                export_data = data.pop(key)
                writer.writerow(self.get_row(key, export_data))
            except KeyError:
                writer.writerow(row)


class AppStoreExport:
    def __init__(self):
        self.writer = AppStoreExportWriter()

    def write_exports(self):
        self.write_downloads_export()
        self.write_impressions_export()
        self.write_conversion_rates_export()

    def proccessed_data(self, exported_data):
        self.data = self.get_row_per_date(exported_data)
        self.downloads = self.get_downloads(self.data)
        self.impressions = self.get_impressions(self.data)
        self.conversion_rates = self.get_conversion_rates(self.data)

    def get_conversion_rates(self, all_data):
        proccessed_data = {}
        for date, aggregation, country, data in self.data_generator(all_data):
            row = proccessed_data.setdefault(date, {}).setdefault(aggregation, {})
            units_paid = (
                data["units_all"] - data["units_browsers"] - data["units_searchers"]
            )
            row[f"{country}_page_view_browsers"] = func.convertion_rate(
                data["units_browsers"], data["page_view_unique_browsers"]
            )
            row[f"{country}_impressions_browsers"] = func.convertion_rate(
                data["units_browsers"], data["impressions_total_unique_browsers"]
            )
            row[f"{country}_searchers"] = func.convertion_rate(
                data["units_searchers"], data["impressions_total_unique_searchers"]
            )
            row[f"{country}_search_ads"] = func.convertion_rate(
                data["downloads_search_ads"], data["impressions_search_ads"]
            )
            row[f"{country}_total_organic_impressions"] = func.convertion_rate(
                data["units_browsers"]
                + data["units_searchers"]
                - data["downloads_search_ads"],
                data["impressions_total_unique_browsers"]
                + self.get_organic_searchers_impressions(data),
            )
            row[f"{country}_impressions_paid"] = func.convertion_rate(
                units_paid,
                data["impressions_total_unique_all"]
                - data["impressions_total_unique_searchers"]
                - data["impressions_total_unique_browsers"],
            )
            row[f"{country}_page_view_paid"] = func.convertion_rate(
                units_paid,
                data["page_view_unique_all"]
                - data["page_view_unique_browsers"]
                - data["page_view_unique_searchers"],
            )
            row[f"{country}_organic_searchers"] = func.convertion_rate(
                data["units_searchers"] - data["downloads_search_ads"],
                data["impressions_total_unique_searchers"]
                - data["impressions_search_ads"]
                * 1.0
                * data["impressions_total_unique_searchers"]
                / data["impressions_total_all"],
            )
        return proccessed_data

    def get_downloads(self, all_data):
        proccessed_data = {}
        for date, aggregation, country, data in self.data_generator(all_data):
            row = proccessed_data.setdefault(date, {}).setdefault(aggregation, {})
            row[f"{country}_all"] = data["units_all"]
            row[f"{country}_searchers"] = data["units_searchers"]
            row[f"{country}_browsers"] = data["units_browsers"]
            row[f"{country}_search_ads"] = data["downloads_search_ads"]
            row[f"{country}_organic_searchers"] = (
                data["units_searchers"] - data["downloads_search_ads"]
            )
            row[f"{country}_organic"] = (
                data["units_browsers"] + row[f"{country}_organic_searchers"]
            )
            row[f"{country}_paid"] = row[f"{country}_all"] - row[f"{country}_organic"]
        return proccessed_data

    def get_impressions(self, all_data):
        proccessed_data = {}
        for date, aggregation, country, data in self.data_generator(all_data):
            row = proccessed_data.setdefault(date, {}).setdefault(aggregation, {})
            row[f"{country}_all"] = data["impressions_total_unique_all"]
            row[f"{country}_searchers"] = data["impressions_total_unique_searchers"]
            row[f"{country}_browsers"] = data["impressions_total_unique_browsers"]
            row[f"{country}_search_ads"] = data["impressions_search_ads"]
            row[
                f"{country}_organic_searchers"
            ] = self.get_organic_searchers_impressions(data)
            row[f"{country}_organic"] = (
                data["impressions_total_unique_browsers"]
                + row[f"{country}_organic_searchers"]
            )
            row[f"{country}_paid"] = (
                data["impressions_total_unique_all"] - row[f"{country}_organic"]
            )
        return proccessed_data

    def get_organic_searchers_impressions(self, data):
        return round(
            (
                data["impressions_total_unique_searchers"]
                - data["impressions_search_ads"]
                * data["impressions_total_unique_searchers"]
                / data["impressions_total_unique_all"]
            )
        )

    def get_row_per_date(self, exported_data):
        proccessed_data = {}
        for key, data in exported_data.items():
            raw_date, country, aggregation = key.split(",")
            proccessed_data.setdefault(raw_date, {}).setdefault(aggregation, {})[
                country
            ] = {
                "impressions_total_all": int(data["impressionsTotalAll"]),
                "impressions_total_browsers": int(data["impressionsTotalBrowsers"]),
                "impressions_total_searchers": int(data["impressionsTotalSearchers"]),
                "impressions_total_unique_all": int(data["impressionsTotalUniqueAll"]),
                "impressions_total_unique_browsers": int(
                    data["impressionsTotalUniqueBrowsers"]
                ),
                "impressions_total_unique_searchers": int(
                    data["impressionsTotalUniqueSearchers"]
                ),
                "page_view_unique_all": int(data["pageViewUniqueAll"]),
                "page_view_unique_browsers": int(data["pageViewUniqueBrowsers"]),
                "page_view_unique_searchers": int(data["pageViewUniqueSearchers"]),
                "units_all": int(data["unitsAll"]),
                "units_browsers": int(data["unitsBrowsers"]),
                "units_searchers": int(data["unitsSearchers"]),
                "taps_search_ads": int(data.get("tapsSearchAds", 0)),
                "impressions_search_ads": int(data.get("impressionsSearchAds", 0)),
                "downloads_search_ads": int(data.get("downloadsSearchAds", 0)),
            }
        return proccessed_data

    def write_conversion_rates_export(self):
        filed_list_params = ["date", *self.get_conversion_rates_field_list()]
        filename_template = "app_store_conversion_rates_{}s.csv"
        self.write_aggregation_exports(
            self.conversion_rates, filename_template, filed_list_params
        )

    def get_conversion_rates_field_list(self):
        return list(
            chain.from_iterable(
                (
                    f"{country}_page_view_browsers",
                    f"{country}_impressions_browsers",
                    f"{country}_searchers",
                    f"{country}_search_ads",
                    f"{country}_total_organic_impressions",
                    f"{country}_impressions_paid",
                    f"{country}_page_view_paid",
                    f"{country}_organic_searchers",
                )
                for country in config.COUNTRIES
            )
        )

    def write_downloads_export(self):
        filed_list_params = ["date", *self.get_downloads_field_list()]
        filename_template = "app_store_downloads_{}s.csv"
        self.write_aggregation_exports(
            self.downloads, filename_template, filed_list_params
        )

    def get_downloads_field_list(self):
        return list(
            chain.from_iterable(
                (
                    f"{country}_all",
                    f"{country}_searchers",
                    f"{country}_browsers",
                    f"{country}_search_ads",
                    f"{country}_organic",
                    f"{country}_organic_searchers",
                )
                for country in config.COUNTRIES
            )
        )

    def write_impressions_export(self):
        filed_list_params = ["date", *self.get_impressions_field_list()]
        filename_template = "app_store_impressions_{}s.csv"
        self.write_aggregation_exports(
            self.impressions, filename_template, filed_list_params
        )

    def get_impressions_field_list(self):
        return list(
            chain.from_iterable(
                (
                    f"{country}_all",
                    f"{country}_searchers",
                    f"{country}_browsers",
                    f"{country}_search_ads",
                    f"{country}_organic",
                    f"{country}_organic_searchers",
                    f"{country}_paid",
                )
                for country in config.COUNTRIES
            )
        )

    def write_aggregation_exports(self, data, filename_template, filed_list_params):
        self.write_export(data, filename_template, filed_list_params, "day")
        self.write_export(data, filename_template, filed_list_params, "week")
        self.write_export(data, filename_template, filed_list_params, "month")

    def write_export(self, data, filename_template, filed_list_params, aggregation):
        aggregation_data = self.get_data_for_aggregation(data, aggregation)
        self.writer.export_data(
            aggregation_data,
            os.path.join(
                config.EXPORTED_DATA_DIR, filename_template.format(aggregation)
            ),
            filed_list_params,
        )

    def get_data_for_aggregation(self, all_data, given_aggregation):
        proccessed_data = {}
        for date, aggregation_data in all_data.items():
            for aggregation, data in aggregation_data.items():
                if aggregation == given_aggregation:
                    proccessed_data[date] = data
        return proccessed_data

    def data_generator(self, all_data):
        for date, aggregation_data in all_data.items():
            for aggregation, country_data in aggregation_data.items():
                for country, data in country_data.items():
                    yield date, aggregation, country, data
