#!/usr/bin/env python3
"""lint-runner: Stop hook that runs linting and blocks until clean."""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TIMEOUT_SECONDS = 60


def get_project_dir() -> Path:
    """Get project directory from env or cwd."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def get_log_path() -> Path:
    """Get lint log file path."""
    log_dir = get_project_dir() / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "lint.log"


def run_lint(command: str) -> tuple[int, str]:
    """Run lint command, return (exit_code, output)."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=get_project_dir(),
        )
        output = result.stdout + result.stderr
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 1, f"Lint timed out after {TIMEOUT_SECONDS} seconds"


def write_failure_log(command: str, exit_code: int, output: str):
    """Write lint failure to log file."""
    log_path = get_log_path()
    timestamp = datetime.now(timezone.utc).isoformat()
    content = f"""================================================================================
LINT FAILED at {timestamp}
Command: {command}
Exit code: {exit_code}
Working directory: {get_project_dir()}
================================================================================

{output}

================================================================================
"""
    log_path.write_text(content)


def clear_failure_log():
    """Remove lint log file if it exists."""
    log_path = get_log_path()
    if log_path.exists():
        log_path.unlink()


def approve():
    """Output approve decision and exit."""
    response = {"decision": "approve"}
    print(json.dumps(response))
    sys.exit(0)


def block():
    """Output block decision with subagent instruction."""
    log_path = get_log_path()
    response = {
        "decision": "block",
        "reason": "Lint failed",
        "systemMessage": (
            f"Lint failed. "
            f"Use the Task tool to spawn a subagent to read {log_path} "
            "and fix all lint errors. The subagent should fix each error "
            "and verify by running the lint command again."
        ),
    }
    print(json.dumps(response))
    sys.exit(0)


def main():
    """Entry point for Stop hook."""
    # Check if lint command is configured
    lint_cmd = os.environ.get("CLAUDE_LINT_COMMAND")
    if not lint_cmd:
        approve()

    # Run lint
    exit_code, output = run_lint(lint_cmd)

    if exit_code == 0:
        clear_failure_log()
        approve()
    else:
        write_failure_log(lint_cmd, exit_code, output)
        block()


if __name__ == "__main__":
    main()
