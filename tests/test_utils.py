import os
from datetime import datetime
from exporter import config
from exporter.utils import func


def test_last_date_in_file(csv_file):
    date = func.get_last_date(datetime(2018, 1, 3), os.path.join(config.RAW_DATA_DIR, "example.csv"))
    assert date == datetime(2019, 9, 3)


def test_calculate_convertion_rate_return_procentage():
    downloads = "4"
    impressions = "10"
    assert func.convertion_rate(downloads, impressions) == 40.0
