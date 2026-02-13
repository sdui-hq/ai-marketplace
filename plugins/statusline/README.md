# Statusline Plugin

## ⚠️ Upgrading from v0.2.0

After updating the plugin **re-run** the setup command to update the script path in your settings:

    /statusline:setup

- **If you had customized sections** in v0.2.0 (by editing the script), those settings now live in `~/.claude/statusline-config.json` and persist across future updates.
- Re-run `/statusline:config` to restore your preferences.

## Features

- **Current Directory**: Shows your working directory
- **Session Name**: Displays the current session name (resolved via Claude Code's internal session index — if this stops working after a Claude Code update, the session name section will gracefully hide itself)
- **Git Branch**: Displays the current git branch
- **Context Window Progress**: Visual progress bar showing context usage
  - Mint (green): < 50% usage
  - Amber (yellow): 50-80% usage
  - Coral (red): > 80% usage

> **Requires `jq`** — If not installed, the statusline shows a fallback with install instructions.

## Installation

### Via Setup Command (Recommended)

After installing the plugin, run the setup command:

```
/statusline:setup
```

This will guide you through configuring the statusline for your Claude Code installation.

### Manual Configuration

Add to your `~/.claude/settings.json` (user-wide) or `.claude/settings.local.json` (project-local):

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/plugins/cache/sdui-marketplace/statusline/<version>/scripts/statusline.sh"
  }
}
```

## Requirements

- **jq**: For parsing JSON input from Claude Code

### Installing Dependencies

macOS:
```bash
brew install jq
```

Ubuntu/Debian:
```bash
sudo apt install jq
```

## Example Output

![Statusline Example](./statusline.png)

## Customization

Run `/statusline:config` to interactively configure which sections appear. Settings are saved to `~/.claude/statusline-config.json` and persist across plugin updates.

Config file format:

```json
{
  "show_session": true,
  "show_branch": true,
  "max_session_len": 30
}
```

Available keys:
- `show_session`: Show session name in statusline (default: `true`)
- `show_branch`: Show git branch in statusline (default: `true`)
- `max_session_len`: Truncate session name after N characters (default: 30, set to 0 for no truncation)

Script-level constants (`BAR_LENGTH`, `SEP`, colors) can be changed by editing the script directly. Note that these will be overwritten on plugin update.

## Troubleshooting

**Statusline not appearing?**
- Restart Claude Code after configuration
- Verify the script path in settings.json is correct

**Git branch not showing?**
- Ensure you're in a git repository
- Check that git is installed and accessible

**Colors not displaying?**
- Ensure your terminal supports 256 colors
- Try setting `TERM=xterm-256color`
