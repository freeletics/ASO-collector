import os
import csv
from unittest import mock
from datetime import datetime
from exporter import config
from exporter.sensortower import export
from exporter.sensortower import export_featured_today
from exporter.sensortower import export_featured_creatives
from exporter.sensortower import export_featured_apps


class TestFeaturedTodayExporter:
    def test_exporting_data(self, featured_today_request, raw_data):
        exporter = export.SensorTowerExport()
        executor = export_featured_today.FeaturedTodayExecutor(exporter)
        executor.execute(datetime.now(), datetime.now())
        filename = os.path.join(
            config.EXPORTED_DATA_DIR, "sensortower_featured_today_ios_days.csv"
        )
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            row = next(reader)
            assert row["app_name"] == "Freeletics"


class TestFeaturedCreativesExporter:
    @mock.patch("exporter.sensortower.utils.Executor.apps", {"a": "ios"})
    def test_exporting_data(self, featured_creative_request, raw_data):
        exporter = export.SensorTowerExport()
        executor = export_featured_creatives.FeaturedCreativesExecutor(exporter)
        executor.execute(datetime.now(), datetime.now())
        filename = os.path.join(
            config.EXPORTED_DATA_DIR, "sensortower_featured_creatives_ios_days.csv"
        )
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            row = next(reader)
            assert row["path"] == "Apps/Fit mit der Apple Watch"


class TestFeaturedAppsExporter:
    def test_exporting_data(self, featured_apps_request, raw_data):
        exporter = export.SensorTowerExport()
        executor = export_featured_apps.FeaturedAppsExecutor(exporter)
        executor.execute(datetime.now(), datetime.now())
        filename = os.path.join(
            config.EXPORTED_DATA_DIR, "sensortower_featured_apps_ios_days.csv"
        )
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            row = next(reader)
            assert row['country'] == "de"
