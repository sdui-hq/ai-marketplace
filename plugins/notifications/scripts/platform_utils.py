#!/usr/bin/env python3
"""Cross-platform utilities for notifications."""

import json
import os
import platform as _platform
import subprocess
import sys
from typing import Literal, Optional

OSType = Literal["linux", "macos", "windows"]
SoundType = Literal["complete", "attention"]

# Linux sound paths (macOS/Windows use native notification sounds)
LINUX_SOUND_PATHS = {
    "complete": "/usr/share/sounds/freedesktop/stereo/complete.oga",
    "attention": "/usr/share/sounds/freedesktop/stereo/message-new-instant.oga",
}

APP_NAME = "Claude Code"


def detect_os() -> OSType:
    """Detect the current operating system."""
    system = _platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Windows":
        return "windows"
    else:
        return "linux"


def get_sound_path(sound_type: SoundType) -> str:
    """Get the sound file path for Linux."""
    return LINUX_SOUND_PATHS[sound_type]


def escape_xml_content(text: str) -> str:
    """Escape special characters for XML content."""
    text = text.replace("&", "&amp;")   # Ampersand first
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def escape_powershell_string(text: str) -> str:
    """Escape special characters for PowerShell double-quoted strings."""
    text = text.replace("`", "``")
    text = text.replace("$", "`$")
    text = text.replace('"', '`"')
    return text


def send_notification(title: str, body: str, urgency: str = "normal") -> bool:
    """Send a desktop notification. Returns True on success."""
    os_type = detect_os()
    try:
        if os_type == "linux":
            cmd = [
                "notify-send",
                "--app-name", APP_NAME,
                "--urgency", urgency,
                title,
                body
            ]
        elif os_type == "macos":
            cmd = ["terminal-notifier", "-title", title, "-message", body, "-sound", "default"]
        else:  # windows
            escaped_title = escape_powershell_string(escape_xml_content(title))
            escaped_body = escape_powershell_string(escape_xml_content(body))
            script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
            $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
            $xml.GetElementsByTagName("text")[0].AppendChild($xml.CreateTextNode("{escaped_title}")) | Out-Null
            $xml.GetElementsByTagName("text")[1].AppendChild($xml.CreateTextNode("{escaped_body}")) | Out-Null
            $audioElement = $xml.CreateElement("audio")
            $audioElement.SetAttribute("src", "ms-winsoundevent:Notification.Default")
            $xml.DocumentElement.AppendChild($audioElement) | Out-Null
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
            '''
            cmd = ["powershell", "-Command", script]

        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def play_sound(sound_type: SoundType) -> bool:
    """Play a notification sound on Linux. macOS/Windows use native notification sounds."""
    sound_path = get_sound_path(sound_type)

    if not os.path.exists(sound_path):
        return False

    try:
        try:
            subprocess.Popen(["paplay", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            subprocess.Popen(["aplay", "-q", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def read_stdin() -> Optional[dict]:
    """Read and parse JSON from stdin."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return None
        return json.loads(data)
    except json.JSONDecodeError:
        return None
