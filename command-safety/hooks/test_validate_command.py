# command-safety/hooks/test_validate_command.py
import pytest
from validate_command import tokenize_command, extract_flags


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
