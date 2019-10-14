import os
from unittest import mock
import pytest
import shutil
from exporter import config
from exporter.play_store import export as play_store_export


@pytest.fixture()
def temp_dir(tmpdir):
    RAW_DATA = "exporter.config.RAW_DATA_DIR"
    EXPORTED_DATA = "exporter.config.EXPORTED_DATA_DIR"
    with mock.patch(RAW_DATA, os.path.join(tmpdir, "raw_data")):
        with mock.patch(EXPORTED_DATA, os.path.join(tmpdir, "exported_data")):
            yield


@pytest.fixture()
def play_store_raw_data(temp_dir):
    os.mkdir(config.RAW_DATA_DIR)
    os.mkdir(config.EXPORTED_DATA_DIR)
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

