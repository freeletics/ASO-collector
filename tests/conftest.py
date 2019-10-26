import os
from unittest import mock
import pytest
import shutil
from exporter import config
from exporter.apps_flyer import export as apps_flyer_export
from exporter.play_store import export as play_store_export


@pytest.fixture()
def temp_dir(tmpdir):
    RAW_DATA = "exporter.config.RAW_DATA_DIR"
    EXPORTED_DATA = "exporter.config.EXPORTED_DATA_DIR"
    with mock.patch(RAW_DATA, os.path.join(tmpdir, "raw_data")):
        with mock.patch(EXPORTED_DATA, os.path.join(tmpdir, "exported_data")):
            yield


@pytest.fixture
def raw_data(temp_dir):
    os.mkdir(config.RAW_DATA_DIR)
    os.mkdir(config.EXPORTED_DATA_DIR)


@pytest.fixture()
def play_store_raw_data(raw_data):
    RAW_DATA_FILE_DIR = os.path.join(config.RAW_DATA_DIR, "play_store.csv")
    RAW_DATA_ORGANIC_FILE_DIR = os.path.join(
        config.RAW_DATA_DIR, "play_store_organic.csv"
    )
    TEST_CSV_FILE_DIR = os.path.join(os.getcwd(), "tests/test_raw_data/play_store.csv")
    shutil.copyfile(TEST_CSV_FILE_DIR, RAW_DATA_FILE_DIR)
    shutil.copyfile(TEST_CSV_FILE_DIR, RAW_DATA_ORGANIC_FILE_DIR)


@pytest.fixture()
def play_store_exporter():
    return play_store_export.PlayStoreExport(
        "play_store.csv", "play_store_organic.csv", "play_store"
    )


@pytest.fixture()
def apps_flyer_installs_report_request(requests_mock):
    return requests_mock.get(
        f"{config.APPS_FLYER_ENDPOINT_BASE}/export/master_report/v4",
        text="""
Install Time,GEO,Installs
2018-02-24,US,4043
2019-05-13,DE,1144
2019-04-07,US,2058
2019-03-30,US,1174
2018-12-24,US,1263
2018-10-23,DE,578
2019-01-28,DE,1706
2018-06-30,US,3628
2018-07-17,US,5124
2019-01-15,US,3893
2019-09-02,DE,1031
2018-03-29,DE,641
2018-08-28,DE,807
2018-10-09,US,2624
2019-04-12,US,1439
2018-05-02,DE,1140
""",
    )


@pytest.fixture()
def apps_flyers_executor():
    exporter = apps_flyer_export.AppsFlyerExport()
    return apps_flyer_export.AppsFlyerExecutor(exporter)
