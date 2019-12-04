import os
import pytest
import json
from unittest import mock
from exporter import config
from exporter.sensortower import export_versions


class TestAppUpdateTimelineExecutor:
    def test_dropping_unwanted_changes_attributes(self, version_request_data):
        executor = export_versions.AppUpdateTimelineExecutor(mock.Mock())
        processed_data = executor.get_processed_data(version_request_data)
        with pytest.raises(KeyError):
            assert processed_data[0]["update_data"][0][1]["featured_user_feedback"]


    def test_exporting_version_data_to_json_file(self, version_request_data, raw_data):
        executor = export_versions.AppUpdateTimelineExecutor(mock.Mock())
        processed_data = executor.get_processed_data(version_request_data)
        executor.write_export(processed_data[0])
        filename = os.path.join(
            config.EXPORTED_DATA_DIR, "sensortower_app_update_timeline_ios_de_days.json"
        )
        with open(filename, mode="r") as file:
            assert type(json.load(file)['update_data']) is list