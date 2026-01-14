import json
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../plugins/notifications/scripts'))

from platform_utils import detect_os, get_sound_path, send_notification, play_sound, read_stdin  # noqa: E402


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
            assert cmd[0] == "terminal-notifier"
            assert "-title" in cmd
            assert "Test Title" in cmd
            assert "-message" in cmd
            assert "Test Body" in cmd
            assert "-sound" in cmd

    @patch("subprocess.Popen")
    def test_windows_notification(self, mock_popen):
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Test Title", "Test Body", "normal")
            mock_popen.assert_called_once()
            cmd = mock_popen.call_args[0][0]
            assert cmd[0] == "powershell"

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

    @patch("subprocess.Popen")
    def test_windows_escapes_dollar_signs(self, mock_popen):
        """Test that dollar signs are escaped to prevent PowerShell variable expansion."""
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", "$env:USERNAME leaked data", "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # Dollar sign should be escaped with backtick
            assert "`$env:USERNAME" in ps_script

    @patch("subprocess.Popen")
    def test_windows_escapes_subexpressions(self, mock_popen):
        """Test that $() subexpressions are escaped to prevent command injection."""
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", "Result: $(Get-Process)", "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # The $( should be escaped
            assert "`$(Get-Process)" in ps_script

    @patch("subprocess.Popen")
    def test_windows_escapes_backticks(self, mock_popen):
        """Test that backticks are escaped since they are PowerShell's escape character."""
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", "Use `n for newline", "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # Backtick should be doubled
            assert "``n" in ps_script

    @patch("subprocess.Popen")
    def test_windows_escapes_double_quotes(self, mock_popen):
        """Test that double quotes are escaped to prevent string breakout."""
        with patch("platform_utils.detect_os", return_value="windows"):
            send_notification("Alert", 'File "test.txt" saved', "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # Quotes should be escaped - XML entity &quot; then PS backtick
            # XML escapes " to &quot;, but we need PS escaping for the string context
            # Since escape_xml_content runs first, " becomes &quot;
            # Then escape_powershell_string runs, but &quot; has no special PS chars
            assert "&quot;test.txt&quot;" in ps_script

    @patch("subprocess.Popen")
    def test_windows_injection_attempt_neutralized(self, mock_popen):
        """Test that command injection attempts are properly neutralized."""
        with patch("platform_utils.detect_os", return_value="windows"):
            # Attempt to break out of string and execute PowerShell
            malicious_body = '"); Remove-Item -Recurse C:\\; Write-Host("'
            send_notification("Alert", malicious_body, "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # The quotes should be XML-escaped, and the whole thing safe
            assert "&quot;)" in ps_script
            # Should not contain unescaped quotes that could break out

    @patch("subprocess.Popen")
    def test_windows_variable_injection_neutralized(self, mock_popen):
        """Test that variable injection is properly neutralized."""
        with patch("platform_utils.detect_os", return_value="windows"):
            # Attempt to inject $xml variable reference to mess with the script
            malicious_body = "Value: $xml.ToString()"
            send_notification("Alert", malicious_body, "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # The dollar sign should be escaped
            assert "`$xml.ToString()" in ps_script

    @patch("subprocess.Popen")
    def test_windows_combined_xml_and_ps_special_chars(self, mock_popen):
        """Test escaping when both XML and PowerShell special chars are present."""
        with patch("platform_utils.detect_os", return_value="windows"):
            # Contains XML special chars (<, &) and PS special chars ($, `)
            body = "<script>$env:USER`n</script>"
            send_notification("Alert", body, "normal")
            cmd = mock_popen.call_args[0][0]
            ps_script = cmd[2]
            # XML entities should be present
            assert "&lt;script&gt;" in ps_script
            # PS special chars should be escaped
            assert "`$env:USER" in ps_script
            assert "``n" in ps_script



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


class TestReadStdin:
    """Test reading and parsing JSON from stdin."""

    def test_valid_json(self):
        data = {"notification_type": "permission_prompt", "message": "Allow?"}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = read_stdin()
        assert result == data

    def test_empty_stdin(self):
        with patch("sys.stdin", StringIO("")):
            result = read_stdin()
        assert result is None

    def test_whitespace_only_stdin(self):
        with patch("sys.stdin", StringIO("   \n  ")):
            result = read_stdin()
        assert result is None

    def test_invalid_json(self):
        with patch("sys.stdin", StringIO("not valid json")):
            result = read_stdin()
        assert result is None

    def test_nested_json(self):
        data = {"stop_hook_data": {"stop_reason": "end_turn", "duration_ms": 1000}}
        with patch("sys.stdin", StringIO(json.dumps(data))):
            result = read_stdin()
        assert result == data
        assert result["stop_hook_data"]["stop_reason"] == "end_turn"
