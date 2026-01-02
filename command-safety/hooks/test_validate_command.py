# command-safety/hooks/test_validate_command.py
import pytest
from validate_command import tokenize_command, extract_flags, match_pattern


class TestTokenizeCommand:
    def test_simple_command(self):
        assert tokenize_command("ls -la") == ["ls", "-la"]

    def test_quoted_string(self):
        assert tokenize_command('echo "hello world"') == ["echo", "hello world"]

    def test_malformed_quotes_fallback(self):
        # Unclosed quote falls back to simple split
        result = tokenize_command('echo "hello')
        assert result == ['echo', '"hello']


class TestExtractFlags:
    def test_combined_flags(self):
        assert extract_flags(["rm", "-rf", "/"]) == {"r", "f"}

    def test_separate_flags(self):
        assert extract_flags(["rm", "-r", "-f", "/"]) == {"r", "f"}

    def test_windows_flags(self):
        assert extract_flags(["del", "/f", "/s"], prefix="/") == {"f", "s"}

    def test_no_flags(self):
        assert extract_flags(["ls", "dir"]) == set()


class TestMatchPattern:
    # command_flags_target
    def test_rm_rf_root(self):
        pattern = {
            "type": "command_flags_target",
            "command": "rm",
            "requires_flags": ["r", "f"],
            "targets": ["/", "~", "*", ".."],
        }
        assert match_pattern(pattern, "rm -rf /") is True
        assert match_pattern(pattern, "rm -fr /") is True
        assert match_pattern(pattern, "rm -r -f /") is True
        assert match_pattern(pattern, "rm -rf /home/user") is False  # safe target
        assert match_pattern(pattern, "rm -r /") is False  # missing -f

    def test_windows_rmdir(self):
        pattern = {
            "type": "command_flags_target",
            "command": "rmdir",
            "requires_flags": ["s", "q"],
            "flag_prefix": "/",
            "targets": None,
        }
        assert match_pattern(pattern, "rmdir /s /q C:\\") is True
        assert match_pattern(pattern, "rmdir /s C:\\") is False  # missing /q

    # command_args
    def test_dd_to_device(self):
        pattern = {
            "type": "command_args",
            "command": "dd",
            "args_contain": ["of=/dev/"],
        }
        assert match_pattern(pattern, "dd if=/dev/zero of=/dev/sda") is True
        assert match_pattern(pattern, "dd if=/dev/zero of=backup.img") is False

    # command_only
    def test_diskpart(self):
        pattern = {"type": "command_only", "command": "diskpart"}
        assert match_pattern(pattern, "diskpart") is True
        assert match_pattern(pattern, "diskpart /s script.txt") is True
        assert match_pattern(pattern, "echo diskpart") is False

    def test_mkfs_variants(self):
        pattern = {"type": "command_only", "command": "mkfs"}
        assert match_pattern(pattern, "mkfs /dev/sda1") is True
        assert match_pattern(pattern, "mkfs.ext4 /dev/sda1") is True
        assert match_pattern(pattern, "mkfs.btrfs /dev/sda1") is True

    # regex
    def test_fork_bomb_regex(self):
        pattern = {
            "type": "regex",
            "pattern": r":\(\)\s*\{.*:\s*\|\s*:.*\}",
            "why": "Fork bomb syntax",
        }
        assert match_pattern(pattern, ":(){ :|:& };:") is True
        assert match_pattern(pattern, ":() { : | : & }; :") is True
        assert match_pattern(pattern, "echo hello") is False
