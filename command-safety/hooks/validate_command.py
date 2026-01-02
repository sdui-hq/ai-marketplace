#!/usr/bin/env python3
"""
command-safety: Pre-execution validator for dangerous bash commands.
Blocks destructive operations before they run.
"""

import json
import os
import re
import shlex
import sys
from datetime import datetime, timezone


def tokenize_command(command: str) -> list[str]:
    """Split command into tokens, handling quotes."""
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def extract_flags(tokens: list[str], prefix: str = "-") -> set[str]:
    """
    Extract all flag characters from tokens.

    "-rf" -> {"r", "f"}
    "-r -f" -> {"r", "f"}
    "/s /q" -> {"s", "q"} (with prefix="/")
    """
    flags = set()
    for token in tokens:
        if token.startswith(prefix) and len(token) > len(prefix):
            flag_chars = token[len(prefix):]
            flags.update(flag_chars)
    return flags


# Dangerous command patterns (MVP)
DANGEROUS_PATTERNS = {
    "file_destruction": [
        # Unix/Mac: rm -rf with dangerous targets
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*)\s+(/|~|\*|\.\.)",
        r"rm\s+(-rf|-fr|-r\s+-f|-f\s+-r)\s+(/|~|\*|\.\.)",
        # Windows: del with force/subdirs/quiet
        r"del\s+/[fsq]+\s+/[fsq]+",
        r"del\s+/f\s+/s",
        # Windows: rmdir/rd with /s /q
        r"(rmdir|rd)\s+/s\s+/q",
        r"(rmdir|rd)\s+/s.*(/q|$)",
    ],
    "disk_overwrite": [
        # Unix: dd writing to device
        r"dd\s+.*if=.*of=/dev/",
        r"dd\s+.*of=/dev/",
        # Unix: mkfs (format)
        r"mkfs(\.[a-z0-9]+)?\s+",
        # Windows: format command
        r"^format\s+[a-zA-Z]:",
        r"\bformat\s+[a-zA-Z]:",
        # Windows: diskpart
        r"diskpart",
    ],
    "fork_bomb": [
        # Unix fork bomb patterns
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",
        r":\(\)\{\s*:\|:&\s*\};:",
        # While true fork patterns
        r"while\s+(true|1|:)\s*;\s*do.*&.*done",
        # Windows batch fork bomb
        r"%0\s*\|\s*%0",
    ],
}


def get_log_path():
    """Get the log file path, creating directory if needed."""
    cwd = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    log_dir = os.path.join(cwd, ".claude", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "command-safety.log")


def log_blocked_command(command: str, pattern_category: str):
    """Log a blocked command attempt to the log file."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command[:500],  # Truncate very long commands
        "pattern": pattern_category,
        "action": "denied",
    }
    try:
        log_path = get_log_path()
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        # Don't fail the hook if logging fails
        pass


def check_dangerous(command: str) -> tuple[bool, str]:
    """
    Check if a command matches any dangerous patterns.
    Returns (is_dangerous, category) tuple.
    """
    for category, patterns in DANGEROUS_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return True, category
    return False, ""


def deny(command: str, category: str, message: str):
    """Output deny response and exit."""
    log_blocked_command(command, category)
    response = {
        "hookSpecificOutput": {"permissionDecision": "deny"},
        "systemMessage": message,
    }
    print(json.dumps(response), file=sys.stderr)
    sys.exit(2)


def main():
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # Can't parse input, allow by default
        sys.exit(0)

    # Extract command
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    # Check for dangerous patterns
    is_dangerous, category = check_dangerous(command)

    if is_dangerous:
        friendly_names = {
            "file_destruction": "Destructive file operation",
            "disk_overwrite": "Disk overwrite operation",
            "fork_bomb": "Fork bomb / resource exhaustion",
        }
        message = f"BLOCKED: {friendly_names.get(category, category)} detected. Command: {command[:100]}"
        deny(command, category, message)

    # Command is safe, allow it
    sys.exit(0)


if __name__ == "__main__":
    main()
