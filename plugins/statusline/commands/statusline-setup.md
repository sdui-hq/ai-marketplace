---
description: Configure statusline for Claude Code
allowed-tools: ["Read", "Write", "Edit", "AskUserQuestion"]
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

If marketplace: Use `~/.claude/plugins/cache/sdui-marketplace/statusline/0.2.0/scripts/statusline.sh`
If local development: Ask user to provide the absolute path to the statusline.sh script.

## Step 4: Customize Sections

Use the AskUserQuestion tool to ask two questions:

**Question 1 (multiSelect):**
- Question: "Which sections do you want to show in the statusline?"
- Header: "Sections"
- multiSelect: true
- Options:
  - Option 1: "Session name (Recommended)" - Description: "Shows the current session name (looked up from Claude's session index)"
  - Option 2: "Git branch (Recommended)" - Description: "Shows the current git branch name"

**Question 2:**
- Question: "Max characters for session name before truncating?"
- Header: "Truncate"
- Options:
  - Option 1: "30 (Recommended)" - Description: "Truncate session names longer than 30 characters"
  - Option 2: "No truncation" - Description: "Show full session name regardless of length"
  - Option 3: "20" - Description: "Truncate session names longer than 20 characters"

The user can also pick "Other" (built into AskUserQuestion) to provide a custom numeric value.

## Step 5: Apply Section Preferences

Read the statusline script at the path determined in Step 3. Using the Edit tool, update the CONFIGURATION variables:

- If the user selected "Session name" in Question 1, set `SHOW_SESSION=true`, otherwise set `SHOW_SESSION=false`
- If the user selected "Git branch" in Question 1, set `SHOW_BRANCH=true`, otherwise set `SHOW_BRANCH=false`
- For Question 2:
  - If "30" was selected, set `MAX_SESSION_LEN=30`
  - If "No truncation" was selected, set `MAX_SESSION_LEN=0`
  - If "20" was selected, set `MAX_SESSION_LEN=20`
  - If the user provided a custom value via "Other", set `MAX_SESSION_LEN=<custom_value>`

Each variable is on its own line in the CONFIGURATION section at the top of the script. Use Edit to replace each line individually.

## Step 6: Merge Configuration

Merge the following statusline configuration into the settings file, preserving any existing settings:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash <SCRIPT_PATH>"
  }
}
```

Replace `<SCRIPT_PATH>` with the determined script path from Step 3.

## Step 7: Write Updated Settings

Write the merged configuration back to the appropriate settings file based on the scope selection with proper JSON formatting.

## Step 8: Confirm Success

After writing the file, confirm to the user:
- Statusline has been configured successfully
- The statusline will appear on the next Claude Code session
- Mention the specific file path based on their scope selection
- Note that the statusline requires `jq` to be installed for full functionality

## Features Summary

The statusline displays:
- Current working directory
- Session name (from Claude's session index)
- Git branch name
- Context window usage with color-coded progress bar:
  - Mint (green): < 50% usage
  - Amber (yellow): 50-80% usage
  - Coral (red): > 80% usage
