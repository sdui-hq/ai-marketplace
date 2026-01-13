import json
import sys
import os
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from notify_finished import main, NOTIFICATION_TITLE


class TestMain:
    @patch("notify_finished.detect_os", return_value="linux")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_with_data_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once_with(NOTIFICATION_TITLE, "Task completed")
        mock_sound.assert_called_once_with("complete")

    @patch("notify_finished.detect_os", return_value="linux")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_with_empty_stdin_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        with patch("sys.stdin", StringIO("")):
            result = main()
        assert result == 0
        mock_notify.assert_called_once_with(NOTIFICATION_TITLE, "Task completed")
        mock_sound.assert_called_once_with("complete")

    @patch("notify_finished.detect_os", return_value="macos")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_on_macos_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once_with(NOTIFICATION_TITLE, "Task completed")
        mock_sound.assert_not_called()

    @patch("notify_finished.detect_os", return_value="windows")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_on_windows_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once_with(NOTIFICATION_TITLE, "Task completed")
        mock_sound.assert_not_called()
