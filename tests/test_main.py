from unittest import mock
from exporter import main


@mock.patch("exporter.main.get_play_store_export")
@mock.patch("exporter.main.get_app_store_export")
@mock.patch("exporter.main.get_apps_flyier_export")
@mock.patch("exporter.main.get_sensortower_export")
def test_run_do_not_fail(
    play_store_mock, app_store_mock, apps_flyier_mock, sensortower_mock
):
    main.run()
    assert play_store_mock.called
    assert app_store_mock.called
    assert apps_flyier_mock.called
    assert sensortower_mock.called
