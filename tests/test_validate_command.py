"""Tests for command-safety validate_command.py pattern matching."""

import pytest

from validate_command import check_dangerous


class TestFileDestruction:
    """Tests for file_destruction pattern category."""

    @pytest.mark.parametrize(
        "command",
        [
            "rm -rf /",
            "rm -rf ~",
            "rm -rf *",
            "rm -rf ..",
            "rm -fr /",
            "rm -r -f /",
            "rm -f -r /",
            "del /f /s /q C:\\",
            "del /f /s",
            "rmdir /s /q C:\\Users",
            "rd /s /q folder",
        ],
    )
    def test_blocks_dangerous_commands(self, command):
        is_dangerous, category = check_dangerous(command)
        assert is_dangerous is True, f"Expected '{command}' to be blocked"
        assert category == "file_destruction"

    @pytest.mark.parametrize(
        "command",
        [
            "rm -rf ./node_modules",
            "rm -rf build/",
            "rm file.txt",
            "rm -r temp_folder",
            "del file.txt",
            "rmdir empty_folder",
            "rm -rf ./dist",
            "rm -rf ./target",
        ],
    )
    def test_allows_safe_commands(self, command):
        is_dangerous, _ = check_dangerous(command)
        assert is_dangerous is False, f"Expected '{command}' to be allowed"


class TestDiskOverwrite:
    """Tests for disk_overwrite pattern category."""

    @pytest.mark.parametrize(
        "command",
        [
            "dd if=/dev/zero of=/dev/sda",
            "dd if=image.iso of=/dev/sdb",
            "dd if=/dev/urandom of=/dev/nvme0n1",
            "mkfs.ext4 /dev/sda1",
            "mkfs /dev/sda",
            "mkfs.xfs /dev/sdb1",
            "format C:",
            "format D:",
            "diskpart",
        ],
    )
    def test_blocks_dangerous_commands(self, command):
        is_dangerous, category = check_dangerous(command)
        assert is_dangerous is True, f"Expected '{command}' to be blocked"
        assert category == "disk_overwrite"

    @pytest.mark.parametrize(
        "command",
        [
            "dd if=input.bin of=output.bin",
            "dd if=/dev/urandom of=random.dat bs=1M count=10",
            "dd if=backup.img of=restored.img",
        ],
    )
    def test_allows_safe_commands(self, command):
        is_dangerous, _ = check_dangerous(command)
        assert is_dangerous is False, f"Expected '{command}' to be allowed"


class TestForkBomb:
    """Tests for fork_bomb pattern category."""

    @pytest.mark.parametrize(
        "command",
        [
            ":(){:|:&};:",
            ":() { :|: & }; :",
            ":(){ :|:& };:",
            "while true; do cat /dev/zero & done",
            "while 1; do yes & done",
            "%0|%0",
        ],
    )
    def test_blocks_dangerous_commands(self, command):
        is_dangerous, category = check_dangerous(command)
        assert is_dangerous is True, f"Expected '{command}' to be blocked"
        assert category == "fork_bomb"

    @pytest.mark.parametrize(
        "command",
        [
            "while true; do echo 'waiting'; sleep 1; done",
            "for i in 1 2 3; do echo $i; done",
            "while true; do date; sleep 60; done",
        ],
    )
    def test_allows_safe_commands(self, command):
        is_dangerous, _ = check_dangerous(command)
        assert is_dangerous is False, f"Expected '{command}' to be allowed"


class TestGeneralSafeCommands:
    """Tests for common safe commands that should never be blocked."""

    @pytest.mark.parametrize(
        "command",
        [
            "ls -la",
            "git status",
            "npm install",
            "python3 script.py",
            "cat file.txt",
            "grep pattern file.txt",
            "find . -name '*.py'",
            "echo 'hello world'",
            "cd /home/user",
            "mkdir new_folder",
            "cp source.txt dest.txt",
            "mv old.txt new.txt",
        ],
    )
    def test_allows_common_commands(self, command):
        is_dangerous, _ = check_dangerous(command)
        assert is_dangerous is False, f"Expected '{command}' to be allowed"
