import pytest
import datetime
from unittest import mock
from requests import exceptions

from exporter import config
from exporter.sensortower import export
from exporter.sensortower import export_ratings

from . import conftest


class TestSensorTowerExport:
    def test_request_data_increase_request_counter(self, rating_three_days_es_request):
        exporter = export.SensorTowerExport()
        exporter.request_data("/ios/review/get_ratings", {})
        assert exporter.request_counter == 1

    def test_request_data_raises_api_calls_limit(self, rating_three_days_es_request):
        TEST_LIMIT = 1
        exporter = export.SensorTowerExport()
        exporter.request_limit = TEST_LIMIT
        with pytest.raises(export.SensorTowerApiCallsLimit):
            exporter.request_data("/ios/review/get_ratings", {})

    @mock.patch("exporter.config.REQUEST_RETRY_DELAY", mock.Mock(returned_value=0))
    @mock.patch(
        "exporter.sensortower.export.SensorTowerExport.get",
        mock.Mock(side_effect=exceptions.HTTPError),
    )
    def test_request_data_retry_request_when_http_exception(self):
        exporter = export.SensorTowerExport()
        with pytest.raises(exceptions.HTTPError):
            exporter.request_data("/ios/review/get_ratings", {})
            assert exporter_get.call_count == config.REQUEST_RETRIES


class TestExportRatings:
    @mock.patch("exporter.config.COUNTRIES", ["ar", "br"])
    @mock.patch("exporter.config.SENSORTOWER_APPS", {"a": "ios", "b": "ios"})
    def test_get_rating_param_list_return_for_country_and_apps(self, rating_executor):
        PRODUCT_LEN_COUNTRY_APPS = 4
        param_list = rating_executor.get_params_list(
            datetime.datetime(2019, 10, 1),
            datetime.datetime(2019, 10, 2),
        )
        platform, params = param_list[0]
        assert len(param_list) == PRODUCT_LEN_COUNTRY_APPS
        assert platform == "ios"
        assert params.get("app_id") is not None
        assert params.get("auth_token") is not None

    def test_get_params_return_platform_and_params(self, rating_executor):
        params = rating_executor.get_params(
            datetime.datetime(2019, 10, 1),
            datetime.datetime(2019, 10, 2),
            "123",
            "ios",
            "pl",
        )
        assert params[0] == "ios"
        assert type(params[1]) is dict

    @mock.patch("exporter.config.COUNTRIES", ["es", "pl"])
    @mock.patch("exporter.sensortower.export_ratings.utils.Executor.apps", {"a": "ios"})
    def test_get_export_data_return_for_all_countries(
        self, rating_three_days_es_request, rating_executor
    ):
        exporter = export.SensorTowerExport()
        param_list = rating_executor.get_params_list(
            datetime.datetime(2019, 10, 1),
            datetime.datetime(2019, 10, 2),
        )
        exported_data = rating_executor.get_export_data(param_list, exporter)
        assert len(exported_data) == 6

    @mock.patch("exporter.config.COUNTRIES", ["pl", "us"])
    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_row_per_date(self, rating_two_day_two_countries, rating_executor):
        proccessed_data = rating_executor.get_row_per_date(rating_two_day_two_countries)
        assert len(proccessed_data.keys()) == 2

    @mock.patch("exporter.config.COUNTRIES", ["pl", "us"])
    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_row_per_date_has_6_values_per_country(
        self, rating_two_day_two_countries, rating_executor
    ):
        proccessed_data = rating_executor.get_row_per_date(rating_two_day_two_countries)
        assert len(proccessed_data[(conftest.TEST_DATE, "ios")]) == 12

    @pytest.mark.skip(reason="Do not calculate differences between days so data make more sense")
    @mock.patch("exporter.config.COUNTRIES", ["pl", "us"])
    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_proccess_data_drop_last_row(
        self, rating_two_day_two_countries, rating_executor
    ):
        proccessed_data = rating_executor.get_proccessed_data(
            rating_two_day_two_countries
        )
        assert len(proccessed_data.keys()) == 1

    @mock.patch("exporter.config.COUNTRIES", ["pl", "us"])
    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_proccess_data_return_platform_and_date_as_a_key(
        self, rating_two_day_two_countries, rating_executor
    ):
        proccessed_data = rating_executor.get_proccessed_data(
            rating_two_day_two_countries
        )
        date, key = next(iter(proccessed_data))
        assert key == "ios"
        assert date == "2019-10-12"

    def test_get_rating_star_cell(self, rating_executor):
        today = {"ES_star_1": 3}
        yesterday = {"ES_star_1": 2}
        rating_start_value = rating_executor.get_rating_star_cell(
            "ES", 1, today, yesterday
        )
        assert rating_start_value[1] == 1

    def test_get_export_field_list(self, rating_executor):
        field_list = rating_executor.get_export_field_list(["pl"])
        assert field_list[0] == "date"
        assert field_list[1] == "pl_average"
        assert field_list[2] == "pl_star_1"
        assert len(field_list) == 7
