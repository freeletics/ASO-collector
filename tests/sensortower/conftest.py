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
def featured_today_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/ios/featured/today/stories",
        json=[
            {
                "country": "DE",
                "date": "2019-10-30T00:00:00Z",
                "stories": [
                    {
                        "position": 1,
                        "id": "1438763550",
                        "url": "https://apps.apple.com/de/story/id1438763550",
                        "title": "Spuktastische Halloween-Spiele",
                        "label": "IM TREND",
                        "short_description": "Unsere gruseligen Favoriten auf einen Blick.",
                        "style": "media",
                        "artwork": {
                            "url": "https://is2-ssl.mzstatic.com/image/thumb/Features118/v4/13/47/19/13471981-94d7-22b8-0aae-0026fbfb791f/source/3524x2160bb.png",
                            "text_colors": ["dae1e1", "becdcc", "aeb4b4", "98a4a3"],
                            "bg_color": "000000",
                            "alpha": False,
                        },
                        "video_preview_url": None,
                        "apps": [
                            {
                                "app_id": 1128464707,
                                "name": "Freeletics",
                                "publisher_id": "305576988",
                                "publisher_name": "Rocketcat LLC",
                                "categories": [6014, 6016, 7014, 7001],
                                "subtitle": None,
                                "icon_url": "https://is3-ssl.mzstatic.com/image/thumb/Purple123/v4/fa/7b/09/fa7b0919-596e-107d-1327-0cc8ac09ab51/AppIcon-0-1x_U007emarketing-0-85-220-7.png/1024x1024bb.png",
                                "offer": {
                                    "action_text": "KAUFEN",
                                    "price": 1698,
                                    "price_formatted": "16,99\xa0€",
                                },
                                "on_card": False,
                            }
                        ],
                        "substyle": None,
                    }
                ],
            }
        ],
    )


@pytest.fixture()
def featured_apps_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/ios/featured/apps",
        json=[
            {
                "category": 6004,
                "country": "DE",
                "date": "2019-10-30T00:00:00Z",
                "sections": [
                    {
                        "position": 4,
                        "id": 1425798485,
                        "title": "Trainier an der frischen Luft",
                        "style": "small",
                        "apps": [
                            {
                                "app_id": 654810212,
                                "name": "Freeletics - Workout & Fitness",
                                "subtitle": "Workouts für jede Gelegenheit",
                                "label": None,
                                "publisher_id": "579309595",
                                "publisher_name": "Freeletics GmbH",
                                "categories": [6013, 6012],
                                "icon_url": "https://is3-ssl.mzstatic.com/image/thumb/Purple113/v4/5b/f8/01/5bf801f1-6072-045d-97a4-cf741a59448c/AppIcon-0-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-7.png/1024x1024bb.png",
                                "artwork_url": "https://is3-ssl.mzstatic.com/image/thumb/Features123/v4/dd/a3/26/dda326af-37b2-4068-395c-b98c3a2a758b/source/4320x1080bb.png",
                                "video_preview_url": None,
                                "offer": {
                                    "price": 0,
                                    "price_formatted": "0,00\xa0€",
                                    "name": None,
                                },
                            }
                        ],
                    }
                ],
            }
        ],
    )


@pytest.fixture()
def version_request_data():
    return [
        {
            "update_data": [
                [
                    "2019-10-18T00:00:00Z",
                    {
                        "version": None,
                        "name": None,
                        "description": None,
                        "price": None,
                        "icon": None,
                        "screenshot": None,
                        "category": None,
                        "support_url": None,
                        "publisher_name": None,
                        "file_size": None,
                        "related_app": None,
                        "minimum_os_version": None,
                        "featured_user_feedback": {"before": [], "after": []},
                        "publisher_id": None,
                        "keyword": None,
                        "country": None,
                        "supported_device": None,
                        "supported_language": None,
                        "apple_watch_enabled": None,
                        "apple_watch_icon": None,
                        "apple_watch_screenshot": None,
                        "imessage_enabled": None,
                        "imessage_icon": None,
                        "imessage_screenshot": None,
                        "top_in_app_purchase": None,
                        "subtitle": None,
                        "promo_text": None,
                    },
                ]
            ],
            "platform": "ios",
            "country": "de",
            "app_info": {"data": "example"},
        }
    ]


@pytest.fixture()
def featured_creative_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/ios/featured/creatives",
        json={
            "features": [
                {
                    "country_name": "Germany",
                    "country": "DE",
                    "category": None,
                    "type": "list",
                    "path": ["Apps", None, "Fit mit der Apple Watch"],
                    "creatives": [],
                    "first_seen_at": None,
                    "positions": [["2019-10-01", [1]]],
                    "downloads": 7,
                    "downloads_share": 1.03,
                    "feature_downloads": [["2019-10-01", 7]],
                    "occurrences": 1,
                },
                {
                    "country_name": "Germany",
                    "country": "DE",
                    "category": 36,
                    "type": "list",
                    "path": ["Apps", "Unsere ❤️-Apps aus 🇩🇪"],
                    "creatives": [],
                    "first_seen_at": None,
                    "positions": [
                        ["2019-10-03", [15]],
                        ["2019-10-04", [15]],
                        ["2019-10-05", [15]],
                        ["2019-10-06", [15]],
                        ["2019-10-07", [15]],
                        ["2019-10-08", [15]],
                        ["2019-10-09", [15]],
                        ["2019-10-10", [15]],
                    ],
                    "downloads": 115,
                    "downloads_share": 16.99,
                    "feature_downloads": [
                        ["2019-10-03", 16],
                        ["2019-10-04", 15],
                        ["2019-10-05", 14],
                        ["2019-10-06", 14],
                        ["2019-10-07", 14],
                        ["2019-10-08", 14],
                        ["2019-10-09", 14],
                        ["2019-10-10", 14],
                    ],
                    "occurrences": 8,
                },
            ]
        },
    )


@pytest.fixture()
def ranking_data_request(requests_mock):
    return requests_mock.get(
        f"{config.SENSORTOWER_ENDPOINT_BASE}/android/category/category_history",
        json={
            "com.freeletics.lite": {
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
