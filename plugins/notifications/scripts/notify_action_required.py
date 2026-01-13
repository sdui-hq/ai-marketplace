#!/usr/bin/env python3
"""
Claude Code Notification Hook - User Action Required
Sends desktop notification when Claude needs user input.
"""

import sys

from platform_utils import send_notification, play_sound, detect_os, read_stdin

URGENCY_MAP = {
    "permission_prompt": "normal",
    "idle_prompt": "normal",
}

TITLE_MAP = {
    "permission_prompt": "Claude Code - Permission Required",
    "idle_prompt": "Claude Code - Awaiting Input",
}

DEFAULT_TITLE = "Claude Code - Action Required"
DEFAULT_MESSAGE = "Claude needs your input"


def get_notification_title(notification_type: str) -> str:
    """Map notification type to title."""
    return TITLE_MAP.get(notification_type, DEFAULT_TITLE)


def get_notification_urgency(notification_type: str) -> str:
    """Map notification type to urgency level."""
    return URGENCY_MAP.get(notification_type, "normal")


def main() -> int:
    """Main entry point for the notification hook."""
    data = read_stdin() or {}

    notification_type = data.get("notification_type", "unknown")
    message = data.get("message", DEFAULT_MESSAGE)

    title = get_notification_title(notification_type)
    urgency = get_notification_urgency(notification_type)

    send_notification(title, message, urgency)
    if detect_os() == "linux":
        play_sound("attention")
    return 0


if __name__ == "__main__":
    sys.exit(main())
