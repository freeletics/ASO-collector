from unittest import mock
from datetime import datetime

from exporter.sensortower import export
from exporter.sensortower import export_rankings


class TestExportRankings:
    @mock.patch("exporter.config.COUNTRIES", ["us", "de"])
    def test_get_param_list_returns_list_query_for_all_countries(
        self, ranking_executor
    ):
        params = ranking_executor.get_params_list(datetime.now(), datetime.now())
        assert params[0][1]["countries"] == "us,de"

    def test_get_export_data_flatten_returned_dict(
        self, ranking_executor, ranking_data_request
    ):
        exporter = export.SensorTowerExport()
        data = ranking_executor.get_export_data([("android", {})], exporter)
        assert type(data[0]["ranking_history"]) is list
        assert data[0]["category"] == "health_and_fitness"
        assert data[0]["chart_type"] == "topselling_free"

    def test_get_proccessed_data_return_row_per_date(
        self, ranking_executor, ranking_data_request
    ):
        exporter = export.SensorTowerExport()
        data = ranking_executor.get_export_data([("android", {})], exporter)
        proccessed_data = ranking_executor.get_proccessed_data(data)
        assert (
            proccessed_data[("2019-10-10", "android")][
                "de_health_and_fitness_topselling_free"
            ]
            == 73
        )

    @mock.patch("exporter.config.COUNTRIES", ["us"])
    @mock.patch("exporter.config.SENSORTOWER_RANKING_CATEGORIES", {'ios': ['category']})
    @mock.patch("exporter.config.SENSORTOWER_RANKING_CHART_TYPES", {'ios': ['chart_type']})
    def test_get_export_field_list_return_proper_column_name(self,ranking_executor):
        filed_list = ranking_executor.get_export_field_list('ios')
        assert len(filed_list) == 2
        assert filed_list[1] == 'us_category_chart_type'

