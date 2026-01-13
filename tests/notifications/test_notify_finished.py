import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from notify_finished import format_duration, build_notification_body, main


class TestFormatDuration:
    def test_milliseconds(self):
        assert format_duration(500) == "500ms"

    def test_seconds(self):
        assert format_duration(5000) == "5.0s"

    def test_minutes(self):
        assert format_duration(125000) == "2m 5s"


class TestBuildNotificationBody:
    def test_full_data(self):
        data = {
            "stop_hook_data": {
                "stop_reason": "end_turn",
                "duration_ms": 5000,
            }
        }
        body = build_notification_body(data)
        assert "Completed" in body
        assert "5.0s" in body

    def test_empty_data(self):
        body = build_notification_body({})
        assert "Completed" in body

    def test_tool_use_reason(self):
        data = {
            "stop_hook_data": {
                "stop_reason": "tool_use",
            }
        }
        body = build_notification_body(data)
        assert "Tool executed" in body

    def test_max_tokens_reason(self):
        data = {
            "stop_hook_data": {
                "stop_reason": "max_tokens",
            }
        }
        body = build_notification_body(data)
        assert "Token limit reached" in body

    def test_stop_sequence_reason(self):
        data = {
            "stop_hook_data": {
                "stop_reason": "stop_sequence",
            }
        }
        body = build_notification_body(data)
        assert "Stop sequence hit" in body


class TestMain:
    @patch("notify_finished.detect_os", return_value="linux")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_with_data_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_called_once_with("complete")

    @patch("notify_finished.detect_os", return_value="linux")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_with_empty_stdin_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        with patch("sys.stdin", StringIO("")):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_called_once_with("complete")

    @patch("notify_finished.detect_os", return_value="macos")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_on_macos_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_not_called()

    @patch("notify_finished.detect_os", return_value="windows")
    @patch("notify_finished.play_sound")
    @patch("notify_finished.send_notification")
    def test_main_on_windows_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_not_called()
