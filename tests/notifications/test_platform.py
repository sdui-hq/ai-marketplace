import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from platform_utils import detect_os, get_sound_path, send_notification, play_sound


class TestDetectOS:
    def test_linux(self):
        with patch("platform_utils._platform.system", return_value="Linux"):
            assert detect_os() == "linux"

    def test_macos(self):
        with patch("platform_utils._platform.system", return_value="Darwin"):
            assert detect_os() == "macos"

    def test_windows(self):
        with patch("platform_utils._platform.system", return_value="Windows"):
            assert detect_os() == "windows"

    def test_unknown_defaults_to_linux(self):
        with patch("platform_utils._platform.system", return_value="FreeBSD"):
            assert detect_os() == "linux"


class TestGetSoundPath:
    """Test Linux sound path resolution. macOS/Windows use native notification sounds."""

    def test_linux_complete(self):
        path = get_sound_path("complete")
        assert path == "/usr/share/sounds/freedesktop/stereo/complete.oga"

    def test_linux_attention(self):
        path = get_sound_path("attention")
        assert path == "/usr/share/sounds/freedesktop/stereo/message-new-instant.oga"


class TestSendNotification:
    @patch("subprocess.Popen")
    def test_linux_notification(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="linux"):
            send_notification("Test Title", "Test Body", "normal")
            mock_popen.assert_called_once()
            cmd = mock_popen.call_args[0][0]
            assert cmd[0] == "notify-send"
            assert "--app-name" in cmd
            assert "Claude Code" in cmd
            assert "--urgency" in cmd
            assert "normal" in cmd
            assert "Test Title" in cmd
            assert "Test Body" in cmd

    @patch("subprocess.Popen")
    def test_linux_critical_urgency(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="linux"):
            send_notification("Alert", "Urgent", "critical")
            cmd = mock_popen.call_args[0][0]
            assert "critical" in cmd

    @patch("subprocess.Popen")
    def test_macos_notification(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="macos"):
            send_notification("Test Title", "Test Body", "normal")
            mock_popen.assert_called_once()
            cmd = mock_popen.call_args[0][0]
            assert cmd[0] == "osascript"
            assert "-e" in cmd

    @patch("subprocess.Popen")
    def test_windows_notification(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Test Title", "Test Body", "normal")
            mock_popen.assert_called_once()
            cmd = mock_popen.call_args[0][0]
            assert cmd[0] == "powershell"

    @patch("subprocess.Popen")
    def test_macos_escapes_quotes_in_body(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="macos"):
            send_notification("Alert", 'File "test.txt" saved', "normal")
            cmd = mock_popen.call_args[0][0]
            script = cmd[2]
            assert '\\"test.txt\\"' in script

    @patch("subprocess.Popen")
    def test_macos_escapes_quotes_in_title(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="macos"):
            send_notification('"Important" Alert', "Body text", "normal")
            cmd = mock_popen.call_args[0][0]
            script = cmd[2]
            assert '\\"Important\\"' in script

    @patch("subprocess.Popen")
    def test_windows_escapes_ampersand_in_body(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", "Tom & Jerry", "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            assert "&amp;" in ps_script

    @patch("subprocess.Popen")
    def test_windows_escapes_angle_brackets(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", "<script>test</script>", "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            assert "&lt;script&gt;" in ps_script


class TestPlaySound:
    """Test Linux sound playback. macOS/Windows use native notification sounds."""

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.Popen")
    def test_linux_uses_paplay(self, mock_popen, mock_exists):
        play_sound("complete")
        cmd = mock_popen.call_args[0][0]
        assert cmd[0] == "paplay"

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.Popen")
    def test_linux_fallback_to_aplay(self, mock_popen, mock_exists):
        mock_popen.side_effect = [FileNotFoundError(), MagicMock()]
        play_sound("complete")
        assert mock_popen.call_count == 2
        cmd = mock_popen.call_args[0][0]
        assert cmd[0] == "aplay"

    @patch("os.path.exists", return_value=False)
    @patch("subprocess.Popen")
    def test_no_sound_if_file_missing(self, mock_popen, mock_exists):
        result = play_sound("complete")
        assert result is False
        mock_popen.assert_not_called()

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.Popen")
    def test_attention_sound(self, mock_popen, mock_exists):
        play_sound("attention")
        cmd = mock_popen.call_args[0][0]
        assert cmd[0] == "paplay"
        assert "message-new-instant.oga" in cmd[1]
