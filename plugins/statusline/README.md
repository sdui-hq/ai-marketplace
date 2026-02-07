# Statusline Plugin

A customizable statusline for Claude Code that displays essential information at a glance.

## Features

- **Current Directory**: Shows your working directory
- **Git Branch**: Displays the current git branch
- **Context Window Progress**: Visual progress bar showing context usage
  - Mint (green): < 50% usage
  - Amber (yellow): 50-80% usage
  - Coral (red): > 80% usage

## Installation

### Via Setup Command (Recommended)

After installing the plugin, run the setup command:

```
/statusline-setup
```

This will guide you through configuring the statusline for your Claude Code installation.

### Manual Configuration

Add to your `~/.claude/settings.json` (user-wide) or `.claude/settings.local.json` (project-local):

```json
{
  "statusline": "bash ~/.claude/plugins/cache/sdui-marketplace/statusline/0.1.0/scripts/statusline.sh"
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

The script can be customized by editing the configuration section:

- `BAR_LENGTH`: Number of segments in the progress bar (default: 10)
- `SEP`: Separator character between sections (default: `|`)
- Colors can be adjusted using ANSI color codes

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
