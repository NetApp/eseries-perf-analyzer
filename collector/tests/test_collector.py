import unittest
from unittest.mock import patch, mock_open, call
import collector

valid_config_data = {
    "username": "admin",
    "password": "admin"
}

class TestCollector(unittest.TestCase):

    # Test whether we called to the correct endpoint
    @patch("collector.requests.Session")
    def test_get_drive_location(self, mock_session):
        sys_id = "0"
        req_url = ("{}/{}/hardware-inventory").format(collector.PROXY_BASE_URL, sys_id)
        
        drive_loc = collector.get_drive_location(sys_id, mock_session)
        mock_session.get.assert_called_with(req_url)


    # Test that we open a valid config file
    @patch("collector.requests")
    @patch("collector.json")
    def test_get_session_valid_config(self, mock_json_load, mock_requests):
        mock_json_load.return_value = valid_config_data
        with patch("collector.open", mock_open()):
            try:
                collector.get_session()
            except:
                self.fail("get_session raised an exception with valid config data")


    # Test that we correctly fail opening an invalid config file
    @patch("collector.requests")
    @patch("collector.json")
    @patch("collector.CMD")
    @patch("collector.LOG")
    def test_get_session_invalid_config(self, mock_log, mock_cmd, mock_json_load, mock_requests):
        mock_json_load.return_value = valid_config_data
        mock_cmd.username = ""
        mock_cmd.password = ""
        with patch("collector.open", mock_open()) as mocked_open:
            mocked_open.side_effect = IOError
            collector.get_session()
            mock_log.exception.assert_called()


    # Test that we call to the correct endpoints for storage stats
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_storage_metrics(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }
        sys_id = system["id"]
        req_url_drive = ("{}/{}/analysed-drive-statistics").format(collector.PROXY_BASE_URL, sys_id)
        req_url_system = ("{}/{}/analysed-system-statistics").format(collector.PROXY_BASE_URL, sys_id)
        req_url_volume = ("{}/{}/analysed-volume-statistics").format(collector.PROXY_BASE_URL, sys_id)

        mock_session = mock_get_session.return_value
        collector.collect_storage_metrics(system)
        
        calls = [call(req_url_drive), call(req_url_system), call(req_url_volume)]

        mock_get_session.assert_called()
        mock_session.get.assert_has_calls(calls, any_order=True)


    # Test that we properly write points to influxdb when collecting storage metrics
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_storage_metrics_writepoints(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }

        mock_session = mock_get_session.return_value
        collector.collect_storage_metrics(system)

        mock_influxclient = mock_influxdb.return_value
        mock_influxclient.write_points.assert_called()


    # Test that we call to the correct endpoints for MEL events
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_major_event_log(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }
        sys_id = system["id"]
        req_url_mel = ("{}/{}/mel-events").format(collector.PROXY_BASE_URL, sys_id)

        mock_session = mock_get_session.return_value
        collector.collect_major_event_log(system)
        
        call_params = {
            "count": 8192,
            "startSequenceNumber": 2
        }

        mock_get_session.assert_called()
        mock_session.get.assert_called_with(req_url_mel, params=call_params)


    # Test that we properly write points to influxdb when collecting mel events
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_major_event_log_writepoints(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }

        mock_session = mock_get_session.return_value
        collector.collect_major_event_log(system)

        mock_influxclient = mock_influxdb.return_value
        mock_influxclient.write_points.assert_called()


    # Test that we call to the correct endpoints for system state
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_system_state(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }
        sys_id = system["id"]
        req_url_fails = ("{}/{}/failures").format(collector.PROXY_BASE_URL, sys_id)

        mock_session = mock_get_session.return_value
        collector.collect_system_state(system)
        
        mock_get_session.assert_called()
        mock_session.get.assert_called_with(req_url_fails)


    # Test that we properly write points to influxdb when collecting system state
    @patch("collector.InfluxDBClient")
    @patch("collector.get_session")
    @patch("collector.requests")
    def test_collect_system_state_writepoints(self, mock_requests, mock_get_session, mock_influxdb):
        system = {
            "id": "0"
        }

        mock_session = mock_get_session.return_value
        collector.collect_system_state(system)

        mock_influxclient = mock_influxdb.return_value
        mock_influxclient.write_points.assert_called()
