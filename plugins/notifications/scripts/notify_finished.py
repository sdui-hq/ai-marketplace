#!/usr/bin/env python3
"""
Claude Code Stop Hook - "When Finished" Notification
Sends desktop notification and plays sound when Claude finishes responding.
"""

import json
import sys
from typing import Optional

from platform_utils import send_notification, play_sound, detect_os

NOTIFICATION_TITLE = "Claude Code - Finished"


def format_duration(ms: int) -> str:
    """Format milliseconds as human-readable duration."""
    if ms < 1000:
        return f"{ms}ms"
    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def read_stdin() -> Optional[dict]:
    """Read and parse JSON from stdin."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return None
        return json.loads(data)
    except json.JSONDecodeError:
        return None


def build_notification_body(data: dict) -> str:
    """Build notification body from stop hook data."""
    stop_data = data.get("stop_hook_data", {})
    parts = []

    reason_map = {
        "end_turn": "Completed",
        "tool_use": "Tool executed",
        "max_tokens": "Token limit reached",
        "stop_sequence": "Stop sequence hit"
    }

    reason = stop_data.get("stop_reason", "end_turn")
    parts.append(f"Status: {reason_map.get(reason, reason)}")

    duration_ms = stop_data.get("duration_ms")
    if duration_ms:
        parts.append(f"Duration: {format_duration(duration_ms)}")

    return "\n".join(parts)


def main() -> int:
    """Main entry point for the stop hook."""
    data = read_stdin() or {}
    body = build_notification_body(data)
    send_notification(NOTIFICATION_TITLE, body)
    if detect_os() == "linux":
        play_sound("complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
