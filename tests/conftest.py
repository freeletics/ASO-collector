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
def csv_file(raw_data):
    EXAMPLE_FILE_DIR = os.path.join(config.RAW_DATA_DIR, "example.csv")
    TEST_CSV_FILE_DIR = os.path.join(os.getcwd(), "tests/test_raw_data/example.csv")
    shutil.copyfile(TEST_CSV_FILE_DIR, EXAMPLE_FILE_DIR)


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
Install Time,GEO,Channel,Installs
2019-09-13,DE,Snapchat,2
2019-10-13,DE,None,570
2019-10-16,US,Facebook,31
2019-09-21,DE,Tinder,1
2019-10-19,US,None,349
2019-09-14,US,Facebook,32
2019-10-17,US,Facebook,33
2019-10-26,US,Instagram,42
2019-10-25,DE,AudienceNetwork,1
2019-10-11,US,AudienceNetwork,2
2019-10-19,US,AudienceNetwork,1
2019-10-19,DE,AudienceNetwork,2
2019-09-19,US,Tinder,21
2019-09-29,DE,Instagram,105
2019-09-08,DE,Instagram,75
2019-10-06,DE,None,614
2019-09-28,US,Instagram,75
2019-09-18,DE,Tinder,36
2019-09-18,US,Facebook,94
2019-09-08,DE,None,739
""",
    )


@pytest.fixture()
def apps_flyers_executor():
    exporter = apps_flyer_export.AppsFlyerExport()
    return apps_flyer_export.AppsFlyerExecutor(exporter)
