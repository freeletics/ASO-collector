import os
from datetime import datetime
from unittest import mock

from exporter import config
from exporter.apps_flyer import export


class TestAppFlyerExecutor:
    @mock.patch("exporter.config.COUNTRIES", ["us", "es"])
    def test_get_params_return_countries_in_upper_case(self):
        executor = export.AppsFlyerExecutor(mock.Mock())
        params = executor.get_params_list(datetime.today(), datetime.today())
        assert params[0][1]["geo"] == "US,ES"

    def test_saving_raw_report(
        self, apps_flyer_installs_report_request, raw_data, apps_flyers_executor
    ):
        apps_flyers_executor.get_export_data([("ios", {})])
        assert (
            os.path.exists(
                os.path.join(config.RAW_DATA_DIR, "apps_flyer_installs_ios.csv")
            )
            is True
        )

    def test_get_export_data_return_list(
        self, apps_flyer_installs_report_request, raw_data, apps_flyers_executor
    ):
        exported_data = apps_flyers_executor.get_export_data([("ios", {})])
        assert exported_data[0]["country"] == "DE"
        assert exported_data[0]["platform"] == "ios"

    def test_get_proccessed_data_return_dict(self, apps_flyers_executor):
        exported_data = [
            {
                "platform": "ios",
                "date": "2018-02-24",
                "country": "US",
                "channel": "None",
                "installs": "4043",
            },
            {
                "platform": "ios",
                "date": "2019-05-13",
                "country": "DE",
                "channel": "None",
                "installs": "1144",
            },
        ]
        proccessed_data = apps_flyers_executor.get_proccessed_data(exported_data)
        assert proccessed_data[("2019-05-13", "ios")] == { "de_organic": 1144}
