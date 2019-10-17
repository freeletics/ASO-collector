from unittest import mock
from exporter import main


@mock.patch("exporter.main.get_play_store_export")
def test_run_do_not_fail(play_store_mock):
    main.run()
    assert play_store_mock.called
