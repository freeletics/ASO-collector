import datetime
import os
import os.path
import pytest
from unittest import mock
from exporter.play_store import export
from exporter.play_store import script
from exporter import config


class TestPlayStoreExport:
    @mock.patch("exporter.config.COUNTRIES", ["ar", "es"])
    def test_reading_raw_data_creates_dictionary(self, play_store_raw_data):
        exporter = export.PlayStoreExport(
            "play_store.csv", "play_store_organic.csv", "export_play_store"
        )
        exporter.read_raw_data()
        assert exporter.raw_data[0]["date"] == "2019-03-01"

    def test_reading_from_not_existing_file_raise(self):
        with pytest.raises(export.NoRawDataForPlayStore):
            exporter = export.PlayStoreExport(
                "play_store.csv", "play_store_organic.csv", "export_play_store"
            )
            exporter.read_raw_data()

    def test_saving_export_creates_new_files(self, play_store_raw_data):
        EXPECTED_KPI = 2
        EXPECTED_AGGREGATIONS = 3
        exporter = export.PlayStoreExport(
            "play_store.csv", "play_store_organic.csv", "export_play_store"
        )
        exporter.read_all()
        exporter.export_downloads()
        exporter.export_convertion_rates()
        assert (
            len(os.listdir(exporter.exported_data_dir))
            == EXPECTED_KPI * EXPECTED_AGGREGATIONS
        )

    @mock.patch("exporter.config.COUNTRIES", ["ar", "br"])
    def test_exported_data_dictrionary(self, play_store_raw_data):
        exporter = export.PlayStoreExport(
            "play_store.csv", "play_store_organic.csv", "export_play_store"
        )
        exporter.read_all()
        assert exporter.downloads["2019-03-01"]["br_organic"] is not None

    def test_export_downloads(self, play_store_raw_data):
        exporter = export.PlayStoreExport(
            "play_store.csv", "play_store_organic.csv", "export_play_store"
        )
        exporter.read_all()
        exporter.export_downloads()
        assert os.path.exists(exporter.files_saved[0]) is True

    def test_saving_export_updates_old_file(self, play_store_raw_data):
        exporter = export.PlayStoreExport(
            "play_store.csv", "play_store_organic.csv", "export_play_store"
        )
        exporter.export_daily({"2019-06-01": {"es": 1, "pr": 2}}, "downloads")
        exporter.export_daily({"2019-06-02": {"es": 4, "pr": 4}}, "downloads")
        with open(exporter.files_saved[0]) as file:
            assert len(file.readlines()) == 3

    @mock.patch("exporter.config.COUNTRIES", ["ar", "br"])
    def test_export_file_header_contains_date_and_countries(self, play_store_exporter):
        assert all(
            [
                a == b
                for a, b in zip(
                    play_store_exporter.get_field_list(), ["date", "ar_organic", "ar_paid", "br_organic", "br_paid"]
                )
            ]
        )

    def test_export_filename(self, play_store_exporter):
        assert play_store_exporter.get_export_filename(
            "downloads", "monthly"
        ) == os.path.join(config.EXPORTED_DATA_DIR, "play_store_downloads_monthly.csv")


class TestPlayStoreScript:
    def test_extracting_date_from_play_store_file_name(self):
        file_name = "retained_installers_com.freeletics_201903_country"
        date = script.get_play_store_report_date(file_name)
        assert date == datetime.datetime(2019, 3, 1)

    def test_extracting_date_from_play_store_file_name_raise_value_error(self):
        file_name = "retained_insta"
        with pytest.raises(ValueError):
            script.get_play_store_report_date(file_name)

    def test_extracting_date_from_play_store_file_name_raise_value_error(self):
        file_name = "retained_installers_com.freeletics_notdate_country"
        with pytest.raises(ValueError):
            script.get_play_store_report_date(file_name)

    def test_download_data_when_newest_data_date_not_provided(self):
        assert script.report_download_condition(None, "file_name") is True

    def test_download_data_when_file_newer_than_newest_data(self):
        assert (
            script.report_download_condition(
                datetime.datetime(2019, 1, 1),
                "retained_installers_com.freeletics_201903_country",
            )
            is True
        )

    def test_do_not_download_data_when_file_older_than_newest_data(self):
        assert (
            script.report_download_condition(
                datetime.datetime(2019, 6, 1),
                "retained_installers_com.freeletics_201903_country",
            )
            is False
        )

    @mock.patch(
        "exporter.play_store.script.get_file_names_from_storage",
        mock.Mock(
            return_value=[
                "retained_installers_com.glovo_201901_play_country.csv",
                "retained_installers_com.glovo_201901_country.csv",
            ]
        ),
    )
    @mock.patch("exporter.play_store.script.download_file_from_storage", mock.Mock())
    def test_download_reports_return_dict_with_data_pairs(self):
        downloads_files = script.download_reports(
            datetime.datetime(2019, 1, 1), mock.Mock()
        )
        assert (
            downloads_files["2019-01"]["total"]
            == "retained_installers_com.glovo_201901_country.csv"
        )
        assert (
            downloads_files["2019-01"]["organic"]
            == "retained_installers_com.glovo_201901_play_country.csv"
        )
