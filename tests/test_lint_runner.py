"""Tests for lint-runner hook."""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch


class TestGetProjectDir:
    """Tests for get_project_dir function."""

    def test_returns_env_var_when_set(self):
        from lint_runner import get_project_dir

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": "/custom/path"}):
            result = get_project_dir()
            assert result == Path("/custom/path")

    def test_returns_cwd_when_env_not_set(self):
        from lint_runner import get_project_dir

        with patch.dict(os.environ, {}, clear=True):
            with patch("os.getcwd", return_value="/current/dir"):
                result = get_project_dir()
                assert result == Path("/current/dir")


class TestGetLogPath:
    """Tests for get_log_path function."""

    def test_returns_correct_path(self, tmp_path):
        from lint_runner import get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            result = get_log_path()
            assert result == tmp_path / ".claude" / "logs" / "lint.log"

    def test_creates_parent_directories(self, tmp_path):
        from lint_runner import get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            result = get_log_path()
            assert result.parent.exists()


class TestRunLint:
    """Tests for run_lint function."""

    def test_returns_exit_code_and_output(self, tmp_path):
        from lint_runner import run_lint

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            exit_code, output = run_lint("echo 'lint output'")
            assert exit_code == 0
            assert "lint output" in output

    def test_captures_stderr(self, tmp_path):
        from lint_runner import run_lint

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            exit_code, output = run_lint("echo 'error' >&2")
            assert "error" in output

    def test_returns_nonzero_on_failure(self, tmp_path):
        from lint_runner import run_lint

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            exit_code, output = run_lint("exit 1")
            assert exit_code == 1

    def test_handles_timeout(self, tmp_path):
        from lint_runner import run_lint

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            # Use a command that would take longer than timeout
            with patch("lint_runner.TIMEOUT_SECONDS", 0.1):
                exit_code, output = run_lint("sleep 10")
                assert exit_code == 1
                assert "timed out" in output.lower()


class TestWriteFailureLog:
    """Tests for write_failure_log function."""

    def test_writes_log_file(self, tmp_path):
        from lint_runner import write_failure_log, get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            write_failure_log("npm run lint", 1, "Some error output")
            log_path = get_log_path()
            assert log_path.exists()
            content = log_path.read_text()
            assert "npm run lint" in content
            assert "Some error output" in content
            assert "Exit code: 1" in content

    def test_overwrites_existing_log(self, tmp_path):
        from lint_runner import write_failure_log, get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            write_failure_log("first command", 1, "first error")
            write_failure_log("second command", 2, "second error")
            log_path = get_log_path()
            content = log_path.read_text()
            assert "first" not in content
            assert "second command" in content
            assert "second error" in content


class TestClearFailureLog:
    """Tests for clear_failure_log function."""

    def test_removes_existing_log(self, tmp_path):
        from lint_runner import clear_failure_log, get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            log_path = get_log_path()
            log_path.write_text("some content")
            assert log_path.exists()
            clear_failure_log()
            assert not log_path.exists()

    def test_handles_missing_log(self, tmp_path):
        from lint_runner import clear_failure_log, get_log_path

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            log_path = get_log_path()
            assert not log_path.exists()
            clear_failure_log()  # Should not raise
            assert not log_path.exists()


class TestApprove:
    """Tests for approve function."""

    def test_outputs_approve_json(self, capsys):
        from lint_runner import approve

        with pytest.raises(SystemExit) as exc_info:
            approve()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        response = json.loads(captured.out)
        assert response == {"decision": "approve"}


class TestBlock:
    """Tests for block function."""

    def test_outputs_block_json_with_message(self, capsys, tmp_path):
        from lint_runner import block

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            with pytest.raises(SystemExit) as exc_info:
                block()
            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            response = json.loads(captured.out)
            assert response["decision"] == "block"
            assert response["reason"] == "Lint failed"
            assert "Task tool" in response["systemMessage"]
            assert ".claude/logs/lint.log" in response["systemMessage"]
