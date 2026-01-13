# notifications

Cross-platform desktop notifications for Claude Code events.

## What it does

This plugin sends desktop notifications:
- **Stop hook**: When Claude finishes responding 
- **Notification hook**: When Claude needs user input 

## Requirements

**Linux:**
- `notify-send` (libnotify) - usually pre-installed
- `paplay` (PulseAudio) or `aplay` (ALSA) for sounds

**macOS:**
- `terminal-notifier` (required): `brew install terminal-notifier`

**Windows:**
- PowerShell 5.0+ (included in Windows 10+)
