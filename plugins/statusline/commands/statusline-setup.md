---
description: Configure statusline for Claude Code
allowed-tools: ["Read", "Write", "AskUserQuestion"]
---

Configure the statusline by updating the appropriate settings file based on chosen scope.

## Step 1: Collect Scope Preference

Use the AskUserQuestion tool to ask the user where to install the configuration:

- Question: "Where should the statusline configuration be installed?"
- Header: "Scope"
- Options:
  - Option 1: "User scope (Recommended)" - Description: "Saves to ~/.claude/settings.json - applies to all your Claude Code sessions"
  - Option 2: "Project scope" - Description: "Saves to .claude/settings.local.json - applies only to this project"

## Step 2: Read Existing Settings

Based on the scope selection from Step 1, read the existing settings file. If the file doesn't exist, start with an empty object `{}`.

| Scope | File Path |
|-------|-----------|
| User scope | `~/.claude/settings.json` |
| Project scope | `.claude/settings.local.json` |

## Step 3: Determine Script Path

The statusline script path depends on where the plugin is installed.

For users who installed via marketplace, the script will be at:
`~/.claude/plugins/cache/sdui-marketplace/statusline/<version>/scripts/statusline.sh`

For users testing locally or developing, suggest they use the absolute path to the script in this repository.

Ask the user which applies:
- Question: "How did you install the statusline plugin?"
- Header: "Install"
- Options:
  - Option 1: "Via marketplace (Recommended)" - Description: "Plugin was installed using Claude Code's plugin install command"
  - Option 2: "Local development" - Description: "Testing locally from the repository"

If marketplace: Use `~/.claude/plugins/cache/sdui-marketplace/statusline/0.1.0/scripts/statusline.sh`
If local development: Ask user to provide the absolute path to the statusline.sh script.

## Step 4: Merge Configuration

Merge the following statusline configuration into the settings file, preserving any existing settings:

```json
{
  "statusline": "bash <SCRIPT_PATH>"
}
```

Replace `<SCRIPT_PATH>` with the determined script path from Step 3.

## Step 5: Write Updated Settings

Write the merged configuration back to the appropriate settings file based on the scope selection with proper JSON formatting.

## Step 6: Confirm Success

After writing the file, confirm to the user:
- Statusline has been configured successfully
- The statusline will appear on the next Claude Code session
- Mention the specific file path based on their scope selection
- Note that the statusline requires `jq` and `gh` CLI to be installed for full functionality

## Features Summary

The statusline displays:
- Current working directory
- Git branch name (clickable link to PR or branch on GitHub)
- Context window usage with color-coded progress bar:
  - Mint (green): < 50% usage
  - Amber (yellow): 50-80% usage
  - Coral (red): > 80% usage
