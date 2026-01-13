#!/usr/bin/env python3
"""
Claude Code Stop Hook - "When Finished" Notification
Sends desktop notification and plays sound when Claude finishes responding.
"""

import sys

from platform_utils import send_notification, play_sound, detect_os, read_stdin

NOTIFICATION_TITLE = "Claude Code - Finished"


def main() -> int:
    """Main entry point for the stop hook."""
    read_stdin()  

    send_notification(NOTIFICATION_TITLE, "Task completed")
    if detect_os() == "linux":
        play_sound("complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
