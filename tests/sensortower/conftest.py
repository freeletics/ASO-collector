import pytest
from unittest import mock

from exporter import config
from exporter.sensortower import export_ratings
from exporter.sensortower import export_reviews
from exporter.sensortower import export_rankings

TEST_DATE = "2019-10-12"
config.SENSORTOWER_REQUEST_DELAY = 0


@pytest.fixture()
def rating_executor():
    return export_ratings.RatingExecutor(mock.Mock())


@pytest.fixture()
def review_executor():
    return export_reviews.ReviewExecutor(mock.Mock())


@pytest.fixture
def ranking_executor():
    return export_rankings.RankingExecutor(mock.Mock())


@pytest.fixture()
def ranking_data_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/android/category/category_history",
        json={
            'com.freeletics.lite': {
                "US": {
                    "health_and_fitness": {
                        "topselling_free": {
                            "graphData": [
                                [1570665600, 148, None],
                                [1570752000, 133, None],
                            ],
                            "todays_rank": 162,
                        }
                    }
                },
                "DE": {
                    "health_and_fitness": {
                        "topselling_free": {
                            "graphData": [
                                [1570665600, 73, None],
                                [1570752000, 72, None],
                            ],
                            "todays_rank": 73,
                        }
                    }
                },
            }
        },
    )


@pytest.fixture()
def review_raw_data():
    return [
        {
            "date": "2019-10-09T00:00:00Z",
            "rating": 4,
            "app_id": 284882215,
            "country": "US",
        },
        {
            "date": "2019-10-09T00:00:00Z",
            "rating": 4,
            "app_id": 284882215,
            "country": "US",
        },
        {
            "date": "2019-10-09T00:00:00Z",
            "rating": 1,
            "app_id": 284882215,
            "country": "US",
        },
        {
            "date": "2019-10-10T00:00:00Z",
            "rating": 2,
            "app_id": 284882215,
            "country": "US",
        },
        {
            "date": "2019-10-10T00:00:00Z",
            "rating": 2,
            "app_id": 284882215,
            "country": "US",
        },
        {
            "date": "2019-10-10T00:00:00Z",
            "rating": 2,
            "app_id": 284882215,
            "country": "DE",
        },
    ]


@pytest.fixture()
def review_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/ios/review/get_reviews",
        json={
            "feedback": [
                {
                    "date": "2019-10-09T00:00:00Z",
                    "rating": 4,
                    "app_id": 284882215,
                    "country": "US",
                },
                {
                    "date": "2019-10-09T00:00:00Z",
                    "rating": 2,
                    "app_id": 284882215,
                    "country": "US",
                },
            ],
            "page_count": 4,
            "total_count": 209,
            "rating_breakdown": [52, 12, 11, 18, 116],
        },
    )


@pytest.fixture()
def rating_three_days_es_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/ios/review/get_ratings",
        json=[
            {
                "app_id": 284882215,
                "country": "ES",
                "date": "2019-10-10T00:00:00Z",
                "breakdown": [5091, 968, 950, 1035, 2595],
                "current_version_breakdown": [5091, 968, 950, 1035, 2595],
                "average": 2.537,
                "total": 10639,
            },
            {
                "app_id": 284882215,
                "country": "ES",
                "date": "2019-10-09T00:00:00Z",
                "breakdown": [5089, 968, 948, 1036, 2591],
                "current_version_breakdown": [5089, 968, 948, 1036, 2591],
                "average": 2.536,
                "total": 10632,
            },
            {
                "app_id": 284882215,
                "country": "ES",
                "date": "2019-10-08T00:00:00Z",
                "breakdown": [5085, 964, 946, 1035, 2590],
                "current_version_breakdown": [5085, 964, 946, 1035, 2590],
                "average": 2.537,
                "total": 10620,
            },
        ],
    )


@pytest.fixture()
def rating_two_day_two_countries():
    return [
        {
            "app_id": 284882215,
            "country": "US",
            "date": f"{TEST_DATE}T00:00:00Z",
            "breakdown": [112979, 36145, 36491, 40773, 128779],
            "current_version_breakdown": [112979, 36145, 36491, 40773, 128779],
            "average": 3.102,
            "total": 355167,
        },
        {
            "app_id": 284882215,
            "country": "US",
            "date": "2019-10-11T00:00:00Z",
            "breakdown": [112845, 36099, 36451, 40725, 128634],
            "current_version_breakdown": [112845, 36099, 36451, 40725, 128634],
            "average": 3.102,
            "total": 354754,
        },
        {
            "app_id": 284882215,
            "country": "PL",
            "date": "2019-10-12T00:00:00Z",
            "breakdown": [112728, 36050, 36401, 40679, 128447],
            "current_version_breakdown": [112728, 36050, 36401, 40679, 128447],
            "average": 3.102,
            "total": 354305,
        },
        {
            "app_id": 284882215,
            "country": "PL",
            "date": "2019-10-11T00:00:00Z",
            "breakdown": [112593, 36017, 36358, 40630, 128209],
            "current_version_breakdown": [112593, 36017, 36358, 40630, 128209],
            "average": 3.101,
            "total": 353807,
        },
    ]
