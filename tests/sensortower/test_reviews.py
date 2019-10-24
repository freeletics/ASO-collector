from unittest import mock

from exporter.sensortower import export
from exporter.sensortower import export_reviews


class TestExportReviews:
    def test_export_data_for_all_pages(self, review_request, review_executor):
        exporter = export.SensorTowerExport()
        param_list = [("ios", {})]
        data = review_executor.get_export_data(param_list, exporter)
        assert review_request.call_count == 4
        assert len(data) == 8

    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_proccessed_data_update_rate_counter(
        self, review_executor, review_raw_data
    ):
        data = review_executor.get_proccessed_data(review_raw_data)
        assert data[("2019-10-09", "ios")]["us_star_4"] == 2

    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_proccessed_data_set_default_values(
        self, review_executor, review_raw_data
    ):
        data = review_executor.get_proccessed_data(review_raw_data)
        assert data[("2019-10-09", "ios")]["us_star_3"] == 0

    @mock.patch("exporter.config.SENSORTOWER_APPS", {"284882215": "ios"})
    def test_get_proccessed_calculate_average(self, review_executor, review_raw_data):
        data = review_executor.get_proccessed_data(review_raw_data)
        assert data[("2019-10-09", "ios")]["us_average"] == 3
