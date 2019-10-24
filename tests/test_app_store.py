from exporter.app_store import export


class TestAppStoreExport:
    def test_get_raw_per_date(self):
        data = {
            '2019-10-10,es,day': {
                "country": "es",
                "date": "2019-04-01T00:00:00.000Z",
                "aggregation": "day",
                "impressionsTotalAll": 143834,
                "impressionsTotalBrowsers": 48362,
                "impressionsTotalSearchers": 81865,
                "impressionsTotalUniqueAll": 72049,
                "impressionsTotalUniqueBrowsers": 29318,
                "impressionsTotalUniqueSearchers": 38401,
                "pageViewUniqueAll": 14824,
                "pageViewUniqueBrowsers": 3769,
                "pageViewUniqueSearchers": 2720,
                "unitsAll": 9344,
                "unitsBrowsers": 645,
                "unitsSearchers": 7953,
                "tapsSearchAds": 5413,
                "impressionsSearchAds": 29437,
                "downloadsSearchAds": 2361
            },
        }
        expoter = export.AppStoreExport()
        data_proccessed = expoter.get_row_per_date(data)
        assert data_proccessed['2019-10-10']['day']['es']['units_all'] == 9344
    
    def test_get_data_for_aggregation(self):
        data = {
            '2010-10-10': {
                'day': {
                    'es': 123
                },
                'week': {
                    'es': 321
                }
            }
        }
        expoter = export.AppStoreExport()
        proccessed_data = expoter.get_data_for_aggregation(data, 'week')
        assert proccessed_data['2010-10-10']['es'] == 321