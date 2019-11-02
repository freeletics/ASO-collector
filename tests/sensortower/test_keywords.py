import os
import csv
import pytest
from unittest import mock
from exporter import config
from exporter.sensortower import export_current_keywords


class TestCurrentKeywordsExecutor:
    def test_creating_export_file_per_country(self, raw_data):
        processed_data = {
            ("2019-10-10", "ios", "pl"): {"app": 1, "sport": 2},
            ("2019-10-10", "ios", "de"): {"app": 2, "sport": 5},
        }
        executor = export_current_keywords.KeywordsExecutor(mock.Mock())
        executor.write_export(processed_data)
        assert len(os.listdir(config.EXPORTED_DATA_DIR)) == 2

    def test_updating_keywords_list_export_file(self, raw_data):
        processed_data = {
            ("2019-10-10", "ios", "de"): {"app": 1, "sport": 2},
            ("2019-10-11", "ios", "de"): {"app": 2, "sport": 5},
        }
        executor = export_current_keywords.KeywordsExecutor(mock.Mock())
        executor.write_export(processed_data)
        filename = os.path.join(
            config.EXPORTED_DATA_DIR, "sensortower_current_keywords_de_ios_days.csv"
        )
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            row = next(reader)
            assert int(row["app"]) == 1
            row = next(reader)
            assert int(row["app"]) == 2
