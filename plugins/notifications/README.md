# notifications

Cross-platform desktop notifications for Claude Code events.

## What it does

This plugin sends desktop notifications:
- **Stop hook**: When Claude finishes responding (shows duration, cost, token counts)
- **Notification hook**: When Claude needs user input (permission prompts, idle prompts)

## Platform Support

| OS | Notifications | Sounds |
|----|---------------|--------|
| Linux | `notify-send` | `paplay` / `aplay` |
| macOS | `osascript` | `afplay` |
| Windows | PowerShell toast | PowerShell SoundPlayer |

## Installation

```bash
/plugin install danielr/notifications
```

## Requirements

**Linux:**
- `notify-send` (libnotify) - usually pre-installed
- `paplay` (PulseAudio) or `aplay` (ALSA) for sounds

**macOS:**
- No additional requirements (uses built-in tools)

**Windows:**
- PowerShell 5.0+ (included in Windows 10+)

## Configuration

Optional environment variables to use custom sound files:

| Variable | Description |
|----------|-------------|
| `CLAUDE_NOTIFY_SOUND_FILE` | Custom sound for task completion |
| `CLAUDE_ACTION_SOUND_FILE` | Custom sound for action required |

## Default Sounds

| OS | Completion | Action Required |
|----|------------|-----------------|
| Linux | `complete.oga` | `message-new-instant.oga` |
| macOS | `Glass.aiff` | `Basso.aiff` |
| Windows | `Windows Notify System Generic.wav` | `Windows Notify Email.wav` |

## Context cost

Zero tokens. Desktop notification only, exits with code 0.
