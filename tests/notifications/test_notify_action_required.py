import json
import sys
import os
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from notify_action_required import get_notification_title, get_notification_urgency, main  # noqa: E402


class TestGetNotificationTitle:
    def test_permission_prompt(self):
        assert get_notification_title("permission_prompt") == "Claude Code - Permission Required"

    def test_idle_prompt(self):
        assert get_notification_title("idle_prompt") == "Claude Code - Awaiting Input"

    def test_unknown(self):
        assert get_notification_title("unknown") == "Claude Code - Action Required"


class TestGetNotificationUrgency:
    def test_permission_prompt_is_normal(self):
        assert get_notification_urgency("permission_prompt") == "normal"

    def test_idle_prompt_is_normal(self):
        assert get_notification_urgency("idle_prompt") == "normal"

    def test_unknown_is_normal(self):
        assert get_notification_urgency("unknown") == "normal"


class TestMain:
    @patch("notify_action_required.detect_os", return_value="linux")
    @patch("notify_action_required.play_sound")
    @patch("notify_action_required.send_notification")
    def test_main_with_permission_prompt_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        data = {"notification_type": "permission_prompt", "message": "Allow file write?"}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once_with(
            "Claude Code - Permission Required",
            "Allow file write?",
            "normal"
        )
        mock_sound.assert_called_once_with("attention")

    @patch("notify_action_required.detect_os", return_value="linux")
    @patch("notify_action_required.play_sound")
    @patch("notify_action_required.send_notification")
    def test_main_with_empty_stdin_on_linux(self, mock_notify, mock_sound, mock_detect_os):
        with patch("sys.stdin", StringIO("")):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        assert "Action Required" in mock_notify.call_args[0][0]
        mock_sound.assert_called_once_with("attention")

    @patch("notify_action_required.detect_os", return_value="macos")
    @patch("notify_action_required.play_sound")
    @patch("notify_action_required.send_notification")
    def test_main_on_macos_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"notification_type": "permission_prompt", "message": "Allow file write?"}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_not_called()

    @patch("notify_action_required.detect_os", return_value="windows")
    @patch("notify_action_required.play_sound")
    @patch("notify_action_required.send_notification")
    def test_main_on_windows_no_sound(self, mock_notify, mock_sound, mock_detect_os):
        data = {"notification_type": "idle_prompt", "message": "Waiting for input"}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = main()
        assert result == 0
        mock_notify.assert_called_once()
        mock_sound.assert_not_called()
