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


def match_pattern(pattern: dict, command: str) -> bool:
    """Match a single pattern against a command."""
    pattern_type = pattern.get("type")

    if pattern_type == "command_flags_target":
        tokens = tokenize_command(command)
        if not tokens:
            return False

        if tokens[0] != pattern["command"]:
            return False

        prefix = pattern.get("flag_prefix", "-")
        flags = extract_flags(tokens, prefix)
        required = set(pattern.get("requires_flags", []))
        if not required.issubset(flags):
            return False

        targets = pattern.get("targets")
        if targets is not None:
            return any(t in tokens for t in targets)
        return True

    elif pattern_type == "command_args":
        tokens = tokenize_command(command)
        if not tokens or tokens[0] != pattern["command"]:
            return False
        return all(arg in command for arg in pattern.get("args_contain", []))

    elif pattern_type == "command_only":
        tokens = tokenize_command(command)
        if not tokens:
            return False
        cmd = tokens[0]
        expected = pattern["command"]
        return cmd == expected or cmd.startswith(expected + ".")

    elif pattern_type == "regex":
        return bool(re.search(pattern["pattern"], command, re.IGNORECASE))

    return False


# Dangerous command patterns (declarative syntax)
DANGEROUS_PATTERNS = {
    "file_destruction": [
        # Unix: rm with recursive + force targeting dangerous paths
        {
            "type": "command_flags_target",
            "command": "rm",
            "requires_flags": ["r", "f"],
            "targets": ["/", "~", "*", ".."],
        },
        # Windows: del with force/subdirs/quiet
        {
            "type": "command_args",
            "command": "del",
            "args_contain": ["/f", "/s"],
        },
        # Windows: rmdir with /s /q
        {
            "type": "command_flags_target",
            "command": "rmdir",
            "requires_flags": ["s", "q"],
            "flag_prefix": "/",
            "targets": None,
        },
        # Windows: rd with /s /q
        {
            "type": "command_flags_target",
            "command": "rd",
            "requires_flags": ["s", "q"],
            "flag_prefix": "/",
            "targets": None,
        },
    ],
    "disk_overwrite": [
        # dd writing to block device
        {
            "type": "command_args",
            "command": "dd",
            "args_contain": ["of=/dev/"],
        },
        # mkfs (any filesystem type)
        {
            "type": "command_only",
            "command": "mkfs",
        },
        # Windows format
        {
            "type": "regex",
            "pattern": r"\bformat\s+[a-zA-Z]:",
            "why": "Need word boundary to avoid matching 'reformat' or similar",
        },
        # Windows diskpart
        {
            "type": "command_only",
            "command": "diskpart",
        },
    ],
    "fork_bomb": [
        # Unix fork bomb :(){ :|:& };:
        {
            "type": "regex",
            "pattern": r":\(\)\s*\{.*:\s*\|\s*:.*\}",
            "why": "Fork bomb uses function definition syntax with special chars - "
                   "no consistent token structure to match declaratively",
        },
        # Infinite spawning loop
        {
            "type": "regex",
            "pattern": r"while\s+(true|1|:)\s*;\s*do.*&.*done",
            "why": "Detects 'while true; do ... & done' where & inside loop "
                   "causes infinite process spawning",
        },
        # Windows batch fork bomb
        {
            "type": "regex",
            "pattern": r"%0\s*\|\s*%0",
            "why": "Batch self-invocation pattern - %0 is script itself, "
                   "piping to itself creates exponential process growth",
        },
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
            if match_pattern(pattern, command):
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
